## Mastra

- ワークフロー
  - **ツールをワークフローの１ステップとしてそのまま定義可能**
    - => ワークフロー化することで、ツール呼び出しを開発者側で制御できるため、確実にツールを使わせることができる！
    - **一般的にエージェントではツール利用が LLM 任せになってしまう**

## setup

``` sh
npm init -y


pnpm install typescript tsx @types/node --save-dev

ni @mastra/core mastra @ai-sdk/anthropic
```

``` sh
npx mastra init
```
