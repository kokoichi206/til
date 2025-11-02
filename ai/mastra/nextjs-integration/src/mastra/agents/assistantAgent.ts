import { Agent } from "@mastra/core/agent";

export const assistantAgent = new Agent({
  name: "assistant",
  instructions:
    "あなたは親切で知識豊富な AI アシスタントンゴ。ユーザーの質問にわかりやすく答えるンゴ！",
  model: "anthropic/claude-sonnet-4-5-20250929",
});
