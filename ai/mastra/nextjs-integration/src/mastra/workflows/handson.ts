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
  outputSchema: z.object({
    text: z.string().describe("要約された回答"),
  }),
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
    })
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
            "Confluence で該当するページが見つかりませんでした。"
          );
        }

        const firstPage = pages[0];
        return { pageId: firstPage.id, expand: "body.storage" };
      },
    })
  )
  .then(confluenceGetPageStep)
  .then(
    createStep({
      id: "prepare-prompt",
      inputSchema: confluenceGetPageStep.outputSchema,
      outputSchema: z.object({
        prompt: z.string().describe("AI アシスタントへの最終プロンプト"),
        originalQuery: z.string(),
        pageTitle: z.string(),
        pageUrl: z.string(),
      }),
      execute: async ({ inputData, getInitData }) => {
        const { page, error } = inputData;
        // ワークフローの最初に設定されたデータに簡単にアクセスできる！
        // getInitData, getStepResult, etc...
        const initData = getInitData();

        if (error || !page || !page.content) {
          return {
            prompt: "ページの内容が取得できませんでした。。。",
            originalQuery: initData.query,
            pageTitle: page?.title || "不明",
            pageUrl: page?.url || "不明",
          };
        }

        const prompt = `以下の Confluence ページの内容に基づいて、ユーザーの質問に答えてください。
ユーザーの質問: ${initData.query}

ページタイトル: ${page.title}
ページ内容:
${page.content}

回答は簡潔でわかりやすく、必要に応じて箇条書きを使用してください。`;

        return {
          prompt,
          originalQuery: initData.query,
          pageTitle: page.title,
          pageUrl: page.url,
        };
      },
    })
  )
  .then(
    createStep({
      id: "assistant-response",
      inputSchema: z.object({
        prompt: z.string().describe("AI アシスタントへの最終プロンプト"),
        originalQuery: z.string(),
        pageTitle: z.string(),
        pageUrl: z.string(),
      }),
      // ワークフローの outputSchema と一致させる必要がある。
      outputSchema: z.object({
        text: z.string(),
      }),
      execute: async ({ inputData }) => {
        try {
          const result = await assistantAgent.generate(inputData.prompt);
          return { text: result.text };
        } catch (error) {
          return {
            text: "エラーが発生しました: " + String(error),
          };
        }
      },
    })
  )
  .commit();
