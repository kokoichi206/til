from dotenv import load_dotenv

from llama_index import SimpleDirectoryReader
from llama_index import ListIndex

load_dotenv()

# Data Source を List[Document] に変換。
documents = SimpleDirectoryReader(input_dir="./data").load_data()
print(type(documents))

# Index の作成。
# Index: https://gpt-index.readthedocs.io/en/stable/module_guides/indexing/index_guide.html
list_index = ListIndex.from_documents(documents)
print(type(list_index))

query_engine = list_index.as_query_engine()
print(type(query_engine))

response = query_engine.query("私は誰ですか？")
print(type(response))

for sentence in response.response.split("。"):
    print(f"{sentence}。")
