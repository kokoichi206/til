import { createTool } from "@mastra/core";
import { z } from "zod";

const CONFLUENCE_BASE_URL = process.env.CONFLUENCE_BASE_URL || "";
const CONFLUENCE_API_TOKEN = process.env.CONFLUENCE_API_TOKEN || "";
const CONFLUENCE_USER_EMAIL = process.env.CONFLUENCE_USER_EMAIL || "";

if (!CONFLUENCE_BASE_URL || !CONFLUENCE_API_TOKEN || !CONFLUENCE_USER_EMAIL) {
  throw new Error(
    "Confluence の環境変数が設定されていません。CONFLUENCE_BASE_URL, CONFLUENCE_API_TOKEN, CONFLUENCE_USER_EMAIL を確認してください。"
  );
}

const getAuthHeaders = (): Record<string, string> => {
  const auth = Buffer.from(
    `${CONFLUENCE_USER_EMAIL}:${CONFLUENCE_API_TOKEN}`
  ).toString("base64");
  return {
    Authorization: `Basic ${auth}`,
    Accept: "application/json",
    "Content-Type": "application/json",
  };
};

const callConfluenceAPI = async ({
  endpoint,
  options = {},
}: {
  endpoint: string;
  options?: RequestInit;
}): Promise<any> => {
  const url = `${CONFLUENCE_BASE_URL}/wiki/rest/api${endpoint}`;
  console.log("url: ", url);

  const response = await fetch(url, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...(options.headers || {}),
    },
  });

  if (!response.ok) {
    console.log("response: ", await response.text());
    throw new Error(
      `Confluence API error: ${response.status} ${response.statusText}`
    );
  }

  return response.json();
};

export const confluenceSearchPagesToolOutputSchema = z.object({
  pages: z.array(
    z.object({
      id: z.string().describe("ページ ID"),
      title: z.string().describe("ページタイトル"),
      url: z.string().describe("ページ URL"),
    })
  ),
  total: z.number().describe("検索結果の総数"),
  error: z.string().optional().describe("エラーメッセージ"),
});

export const confluenceSearchPagesTool = createTool({
  id: "confluence-search-pages",
  description: "Confluence でページ検索をする (CQL クエリ対応)",
  inputSchema: z.object({
    cql: z.string().describe("CQL (Confluence Query Language) 検索クエリ"),
  }),
  outputSchema: confluenceSearchPagesToolOutputSchema,
  execute: async ({ context }) => {
    const params = new URLSearchParams();
    params.append("cql", context.cql);

    try {
      const data = await callConfluenceAPI({
        endpoint: `/search?${params.toString()}`,
      });
      const pages = data.results.map((result: any) => ({
        id: result.content?.id,
        title: result.content?.title,
        url: result.url
          ? `${CONFLUENCE_BASE_URL}/wiki${result.url}`
          : undefined,
      }));
      return { pages, total: data.size };
    } catch (error) {
      return { pages: [], total: 0, error: (error as Error).message };
    }
  },
});

export const confluenceGetPageToolOutputSchema = z.object({
  page: z.object({
    id: z.string().describe("ページ ID"),
    title: z.string().describe("ページタイトル"),
    url: z.string().describe("ページ URL"),
    content: z.string().describe("ページ内容 (HTML フォーマット)"),
  }),
  error: z.string().optional().describe("エラーメッセージ"),
});

export const confluenceGetPageTool = createTool({
  id: "confluence-get-page",
  description: "Confluence でページの内容を取得する",
  inputSchema: z.object({
    pageId: z.string().describe("取得したいページの ID"),
    expand: z
      .string()
      .optional()
      .describe(
        "追加で取得したい情報 (例: body.storage, version, ancestors など)"
      ),
  }),
  outputSchema: confluenceGetPageToolOutputSchema,
  execute: async ({ context }) => {
    const { pageId, expand } = context;
    const params = new URLSearchParams();
    if (expand) {
      params.append("expand", expand);
    }

    try {
      const data = await callConfluenceAPI({
        endpoint: `/content/${pageId}?${params.toString()}`,
      });
      const page = {
        id: data.id,
        title: data.title,
        url: `${CONFLUENCE_BASE_URL}/wiki${data._links.webui}`,
        content: data.body?.storage?.value || "",
      };
      return { page };
    } catch (error) {
      return {
        page: {
          id: "",
          title: "",
          url: "",
          content: "",
        },
        error: (error as Error).message,
      };
    }
  },
});
