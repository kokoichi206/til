## Sample

- [LlamaIndexを完全に理解するチュートリアル その１：処理の概念や流れを理解する基礎編（v0.7.9対応）](https://dev.classmethod.jp/articles/llamaindex-tutorial-001-overview-v0-7-9/)

``` sh
pip install llama-index
pip install python-dotenv


pip freeze | grep -e "openai" -e "llama-index" -e "langchain"

langchain==0.0.330
llama-index==0.8.64.post1
openai==1.1.1
```

## Index

- 構成要素
  - Storage Context
    - Vector Store
    - Document Store
    - Index Store
  - Service Context
- [Service Context](https://docs.llamaindex.ai/en/stable/api_reference/service_context.html)
  - Embeddings
    - OpenAI のものではなく LangchainEmbedding などを使うと、Hagging Face などのより広範なモデルに対応できそう
- Query Engine
  - Index class から `as_query_engine` で作成されるクラス
  - 設定項目？
    - retriever_mode
    - node_postprocessors
    - response_synthesizer
    - response_mode
    - prompt templates
- CallbackManager
  - [CBEventType](https://gpt-index.readthedocs.io/en/latest/api_reference/callbacks.html#llama_index.callbacks.CBEventType): 処理フェーズ (ライフサイクル的なやつ)
  - 動作解析やデバッグに役立ちそう
