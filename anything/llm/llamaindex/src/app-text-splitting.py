from llama_index import ListIndex
from llama_index import SimpleDirectoryReader
from llama_index import Document
from llama_index import GPTListIndex
from llama_index import ServiceContext
from llama_index.node_parser import SimpleNodeParser
from llama_index.langchain_helpers.text_splitter import TokenTextSplitter
from llama_index.constants import DEFAULT_CHUNK_OVERLAP, DEFAULT_CHUNK_SIZE
import tiktoken


documents = SimpleDirectoryReader(input_dir="./data").load_data()

# チャンク分割を担う TextSplitter のカスタマイズ。
text_splitter = TokenTextSplitter(
    # str に対する split による分割。
    separator="\n",
    # separator="#",
    chunk_size=200,
    # chunk_size=DEFAULT_CHUNK_SIZE,
    # 前のチャンクの末尾を付与し、チャンク分割による文脈の断裂を緩和。
    chunk_overlap=50,
    # chunk_overlap=DEFAULT_CHUNK_OVERLAP,
    tokenizer=tiktoken.get_encoding("gpt2").encode,
)
node_parser = SimpleNodeParser(text_splitter=text_splitter)

service_context = ServiceContext.from_defaults(
    node_parser=node_parser,
)

# list_index = ListIndex.from_documents(documents)

# https://gpt-index.readthedocs.io/en/stable/api_reference/indices/list.html#llama_index.indices.list.SummaryIndex.from_documents
list_index = GPTListIndex.from_documents(
    documents,
    service_context=service_context,
)

# query_engine = list_index.as_query_engine()

# ノードの分割状況を可視化する。
for doc_id, node in list_index.storage_context.docstore.docs.items():
    node_dict = node.__dict__
    # print(type(node))
    # print(node_dict)
    # start=None, end=None for all nodes...
    # ref: https://gpt-index.readthedocs.io/en/latest/api_reference/node.html#llama_index.schema.Document.start_char_idx
    print(f'{doc_id=}, len={len(node_dict["text"])}, start={node_dict["start_char_idx"]}, end={node_dict["end_char_idx"]}')
