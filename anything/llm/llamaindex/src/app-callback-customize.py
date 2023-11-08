from typing import Dict, List, Any, Optional

from llama_index.callbacks import CBEventType
from llama_index import SimpleDirectoryReader
from llama_index import ListIndex
from llama_index import ServiceContext
from llama_index.callbacks.base import BaseCallbackHandler
from llama_index.callbacks import CallbackManager, LlamaDebugHandler

documents = SimpleDirectoryReader(input_dir="./data").load_data()


class MyCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        event_starts_to_ignore: Optional[List[CBEventType]] = None,
        event_ends_to_ignore: Optional[List[CBEventType]] = None,
        print_trace_on_end: bool = True,
    ) -> None:
        event_starts_to_ignore = event_starts_to_ignore if event_starts_to_ignore else []
        event_ends_to_ignore = event_ends_to_ignore if event_ends_to_ignore else []
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore,
            event_ends_to_ignore=event_ends_to_ignore,
        )

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any
    ) -> str:
        print(f"event_type = {event_type} (start)")
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[Dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any
    ) -> None:
        print(f"event_type = {event_type} (end)")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        print("start_trace")

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        print("end_trace")

# 用意されてるデバッグ用ハンドラー。
llama_debug_handler = LlamaDebugHandler()
# 独自ハンドラー。
my_handler = MyCallbackHandler()
callback_manager = CallbackManager([llama_debug_handler, my_handler])
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
