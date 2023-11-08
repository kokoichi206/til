from llama_index import SimpleDirectoryReader
from llama_index import ListIndex
from llama_index import ServiceContext
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.callbacks import CBEventType

documents = SimpleDirectoryReader(input_dir="./data").load_data()

# 用意されてるデバッグ用ハンドラー。
llama_debug_handler = LlamaDebugHandler()
callback_manager = CallbackManager([llama_debug_handler])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)

list_index = ListIndex.from_documents(
    documents=documents,
    service_context=service_context,
)

query_engine = list_index.as_query_engine()

response = query_engine.query("私について教えて。")

# node_list = llama_debug_handler.get_event_pairs(CBEventType.RETRIEVE)[0][1].payload["nodes"]
# どの Node が選ばれたのかを確認する。
node_list = response.source_nodes
for node in node_list:
    print(f"doc_id ={node.node.id_}")

# LLM へ投げる実際のプロンプトやレスポンスが確認できる。
print(llama_debug_handler.get_event_time_info(CBEventType.LLM))

for i in response.response.split("。"):
    print(i + "。")
