import { createTool } from "@mastra/core";
import { title } from "process";

import { z } from "zod";

const GITHUB_TOKEN = process.env.GITHUB_TOKEN || "";

if (!GITHUB_TOKEN) {
  throw new Error(
    "GitHub の環境変数が設定されていません。GITHUB_TOKEN を確認してください。"
  );
}

export const githubCreateIssueTool = createTool({
  id: "github-create-issue",
  description:
    "GitHub 上で複数の Issue を作成します。バグ報告、機能要求、質問等に使用できます。",
  inputSchema: z.object({
    owner: z.string().describe("リポジトリの所有者のユーザー名"),
    repo: z.string().describe("リポジトリ名"),
    issues: z.array(
      z
        .object({
          title: z.string().describe("Issue のタイトル"),
          body: z.string().describe("Issue の詳細な説明"),
        })
        .describe("作成する Issue のリスト")
    ),
  }),
  outputSchema: z.object({
    success: z.boolean(),
    createdIssues: z.array(
      z.object({
        issueNumber: z.number().describe("作成された Issue の番号"),
        issueUrl: z.string().describe("作成された Issue の URL"),
        title: z.string().describe("Issue のタイトル"),
      })
    ),
  }),
  execute: async ({ context }) => {
    const { owner, repo, issues } = context;
    const createdIssues: Array<{
      issueNumber: number;
      issueUrl: string;
      title: string;
    }> = [];

    for (const issue of issues) {
      const response = await fetch(
        `https://api.github.com/repos/${owner}/${repo}/issues`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${GITHUB_TOKEN}`,
            Accept: "application/vnd.github+json",
          },
          body: JSON.stringify({
            title: issue.title,
            body: issue.body,
          }),
        }
      );

      if (!response.ok) {
        throw new Error(
          `GitHub API error: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      createdIssues.push({
        issueNumber: data.number,
        issueUrl: data.html_url,
        title: data.title,
      });
    }

    return {
      success: true,
      createdIssues,
    };
  },
});
