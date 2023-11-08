from llama_index import SimpleDirectoryReader
from llama_index import ListIndex
from llama_index import ServiceContext
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.callbacks import CBEventType
from llama_index.indices.list.base import ListRetrieverMode

documents = SimpleDirectoryReader(input_dir="./data").load_data()

llama_debug_handler = LlamaDebugHandler()
callback_manager = CallbackManager([llama_debug_handler])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)

list_index = ListIndex.from_documents(
    documents=documents,
    service_context=service_context,
)

# 埋め込みベクトルを計算。
for doc_id, node in list_index.storage_context.docstore.docs.items():
    service_context.embed_model.queue_text_for_embedding(
        doc_id, node.text
    )
result_ids, result_embeddings = service_context.embed_model.get_queued_text_embeddings()

id_to_embed_map = {}
for new_id, text_embedding in zip(result_ids, result_embeddings):
    id_to_embed_map[new_id] = text_embedding

# ノードの embedding 属性に埋め込みベクトルを格納。
node_list = []
for doc_id, node in list_index.storage_context.docstore.docs.items():
    node.embedding = id_to_embed_map[doc_id]
    node_list.append(node)

# 修正したノードでインデックスを再構成。
_ = list_index.build_index_from_nodes(node_list)

# ---------------------- query ----------------------

# # default
# query_engine = list_index.as_query_engine()

# クエリとの類似度が高い順位ノード3つ選択する。
query_engine = list_index.as_query_engine(
    retriever_mode=ListRetrieverMode.EMBEDDING,
    similarity_top_k=3,
)

response = query_engine.query("私はどんな人ですかね。")

node_list = llama_debug_handler.get_event_pairs(CBEventType.RETRIEVE)[0][1].payload["nodes"]

node_count = len(node_list)
print(f"{node_count=}")

# 使用されるノードの選択状況。
# デフォルトでは全ノードを使っている。
for node in node_list:
    doc_id = node.node.id_
    score = node.score
    print(f"{doc_id=}, {score=}")
