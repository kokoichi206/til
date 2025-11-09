import { createStep, createWorkflow } from "@mastra/core";
import {
  confluenceSearchPagesTool,
  confluenceGetPageTool,
  confluenceSearchPagesToolOutputSchema,
  confluenceGetPageToolOutputSchema,
} from "../tools/conflienceTool";
import z from "zod";
import { assistantAgent } from "../agents/assistantAgent";
import { githubCreateIssueTool } from "../tools/githubTool";

const confluenceSearchPageStep = createStep(confluenceSearchPagesTool);
const confluenceGetPageStep = createStep(confluenceGetPageTool);
const githubCreateIssueStep = createStep(githubCreateIssueTool);

export const handsonWorkflow = createWorkflow({
  id: "handson-workflow",
  description: "Confluence のページを検索して内容を取得するワークフロー",
  inputSchema: z.object({
    query: z.string().describe("検索したい内容を自然言語で入力してください。"),
    owner: z.string().describe("GitHub リポジトリの所有者のユーザー名"),
    repo: z.string().describe("GitHub リポジトリ名"),
  }),
  outputSchema: githubCreateIssueTool.outputSchema,
})
  .then(
    createStep({
      id: "confluence-cql-step",
      inputSchema: z.object({
        query: z.string(),
        owner: z.string(),
        repo: z.string(),
      }),
      outputSchema: z.object({
        cql: z.string().describe("生成された CQL クエリ"),
      }),
      execute: async ({ inputData }) => {
        const prompt = `
以下の自然言語の検索要求を Confluence CQL (Confluence Query Language) クエリに変換してください。
CQL の基本的な構文
- text ~ "検索語": 全文検索
- title ~ "検索語": タイトル検索
- space = "SPACEKEY": スペースの指定
- type = "page": ページのみ検索
- created > "YYYY/MM/DD": 作成日でフィルタリング

検索要求: "${inputData.query}"

重要：
- 単純な単語検索の場合は、text ~ "単語" の形式を使用
- 複数の単語を含む場合は OR で結合（この段階では広くヒットさせる）
- 日本語の検索語もそのまま使用可能
- レスポンスは CQL クエリのみを返してください
- \`\`\` などのコーディングブロックは不要です

CQL クエリ:
      `;

        try {
          const result = await assistantAgent.generate(prompt);
          const cql = result.text.trim();
          console.log("cql in handson.ts:", cql);
          return { cql };
        } catch (error) {
          const fallbackCql = `text ~ "${inputData.query}"`;
          return { cql: fallbackCql };
        }
      },
    }),
  )
  .then(confluenceSearchPageStep)
  .then(
    createStep({
      id: "select-first-page",
      inputSchema: confluenceSearchPagesToolOutputSchema,
      outputSchema: z.object({
        pageId: z.string().describe("選択されたページの ID"),
        expand: z.string().optional(),
      }),
      execute: async ({ inputData }) => {
        const { pages, error } = inputData;
        if (error) {
          throw new Error(`Confluence 検索エラー: ${error}`);
        }
        if (!pages || pages.length === 0) {
          throw new Error(
            "Confluence で該当するページが見つかりませんでした。",
          );
        }

        const firstPage = pages[0];
        return { pageId: firstPage.id, expand: "body.storage" };
      },
    }),
  )
  .then(confluenceGetPageStep)
  .then(
    createStep({
      id: "create-development-tasks",
      // Confluenceページ取得ツールのoutputSchemaをそのまま指定
      inputSchema: confluenceGetPageTool.outputSchema,
      // GitHub Issues作成ツールのinputSchemaをそのまま指定
      outputSchema: githubCreateIssueTool.inputSchema,
      execute: async ({ inputData, getInitData }) => {
        // 前のステップから受け渡されるConfluenceのページ情報
        const { page, error } = inputData;
        // GitHubのリポジトリ情報はワークフローの初期データから取得
        const { owner, repo, query } = getInitData();

        // いずれかの情報が取れない場合はエラーメッセージを送信
        if (error || !page || !page.content) {
          return {
            owner: owner || "",
            repo: repo || "",
            issues: [
              {
                title: "エラー: ページの内容が取得できませんでした",
                body: "Confluenceページの内容を取得できませんでした。",
              },
            ],
          };
        }
        // エージェントからの出力フォーマットを規定
        const outputSchema = z.object({
          issues: z.array(
            z.object({
              title: z.string(),
              body: z.string(),
            }),
          ),
        });
        // プロンプト
        const analysisPrompt = `以下のConfluenceページの内容は要件書です。この要件書を分析して、開発バックログのGitHub Issueを複数作成するための情報を生成してください。
ユーザーの質問: ${query}
ページタイトル: ${page.title}
ページ内容:
${page.content}
重要：
- 要件書の内容を機能やコンポーネント単位で分割
- 各Issueのtitleは簡潔で分かりやすく
- bodyはMarkdown形式で構造化
- フォーマットはJSON配列形式で、必ず出力。枕詞は不要。トップの配列は必ず角括弧で囲む。
- \`\`\`jsonのようなコードブロックは不要
- 2つIssueを作成
- 曖昧な部分は「要確認」として記載`;

        try {
          const result = await assistantAgent.generate(analysisPrompt, {
            output: outputSchema, // エージェントからの出力フォーマットを指定
          });
          // JSONからIssueの配列を取り出す
          const parsedResult = JSON.parse(result.text);
          const issues = parsedResult.issues.map(
            (issue: { title: string; body: string }) => ({
              title: issue.title,
              body: issue.body,
            }),
          );
          return {
            owner: owner || "",
            repo: repo || "",
            issues: issues,
          };
        } catch (error) {
          return {
            owner: owner,
            repo: repo,
            issues: [
              {
                title: "エラー: Issue作成に失敗",
                body: "エラーが発生しました: " + String(error),
              },
            ],
          };
        }
      },
    }),
  )
  .then(githubCreateIssueStep)
  .commit();
