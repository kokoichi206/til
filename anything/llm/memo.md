## なにか

- [LangChain](https://www.langchain.com/)
  - [Blog](https://blog.langchain.dev/)
- LlamaIndex
  - 事前学習済み LLM をプライベートなデータで拡張することに特化

## ChatGPT

- 強み
  - 膨大な知識量
- 弱み
  - 非公開情報やドメイン知識に対応できない
- ファインチューニング
- Embedding
  - 文章の類似度を測る仕組み

- 機密性の高いデータを組み込む方法 (一般 llm)
  - 学習段階から学習データに入れておく
  - 学習済みのモデルからのファインチューニング
  - プロンプトにコンテキストとして入力する

## RAG: Retrieval Augmented Generation

[LlamaIndex](https://gpt-index.readthedocs.io/en/latest/getting_started/concepts.html)

## 活用事例

- 誤字脱字の修正
  - https://developer.feedforce.jp/entry/2023/09/29/100000
- 社内ナレッジに即して業務サポートをする側近
  - https://ndigi.tech/all_post/25752

## ベクトルデータベース

- [ベクトルデータベースとは (AWS)](https://aws.amazon.com/jp/what-is/vector-databases/)
- k-最近傍 (k-NN) インデックス
  - [Open Search での k-nn 検索](https://docs.aws.amazon.com/ja_jp/opensearch-service/latest/developerguide/knn.html#knn-settings)
- [pgvector](https://github.com/pgvector/pgvector)

## [Building RAG-based LLM Applications for Production](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1)

``` sh
export EFS_DIR=/Users/kokoichi/ghq/github.com/kokoichi206/til/anything/llm
export EFS_DIR=/...

wget -e robots=off --recursive --no-clobber --page-requisites \
  --html-extension --convert-links --restrict-file-names=windows \
  --domains docs.ray.io --no-parent --accept=html \
  -P $EFS_DIR https://docs.ray.io/en/master/
```

- Agent
  - QueryAgent
- Prompt engineering
  - x-of-thought
  - multimodel
  - self--refine
  - query decomp
  - etc
- [BM25](https://en.wikipedia.org/wiki/Okapi_BM25)
  - Ranking function
- [Ray](https://github.com/ray-project/ray)
  - Ray is a unified framework for scaling AI and Python applications

``` sh
export OPENAI_API_KEY='sk-xxx'
export OPENAI_MODEL_NAME=gpt-3.5-turbo
export OPENAI_TEMPERATURE=0.0

# use python < 3.11
# https://github.com/langchain-ai/langchain/issues/10314
pyenv global 3.10.13

streamlit run app.py --server.port 8080

#   `openai` has no `ChatCompletion` attribute, this is likely due to an old version of the openai package.
# https://github.com/langchain-ai/langchain/issues/12949
pip install openai==0.28.1
pip install langchain==0.0.330
```

## Links

- [Building RAG-based LLM Applications for Production](https://www.anyscale.com/blog/a-comprehensive-guide-for-building-rag-based-llm-applications-part-1)
- [ベクトル検索で欲しい情報が得られないときの問題点と改良方法を考えてみた](https://dev.classmethod.jp/articles/problem-and-improve-methods-of-vector-search/)
  - RAG でのいい感じの図あり
  - 「以外」「数字の大小」？
- [「脱ブラックボックス化！LLMと一緒に使われるLangChainやLlamaIndexを徹底解説」というタイトルでDevelopersIO 2023に登壇しました](https://dev.classmethod.jp/articles/openai-langchain-llamaindex-devio2023/)
