from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import AspectCritic
from ragas.llms import LangchainLLMWrapper


load_dotenv()

# user_input = "日本の首都はどこでしょう＞？？"
user_input = "日本の首都はどこでしょう＞？？質問に端的に回答してください。"

llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
)
response = llm.invoke(("human", user_input)).content
print(response)

sample = SingleTurnSample(
    user_input=user_input,
    response=response,
    reference="東京都",
)

####################
# 評価者
####################
definition = """
参照データと回答を比較し、正確性を評価してください。
参照データに対して、冗長でなく端的かつ関連した回答ができた場合のみ、評価値を1としてください。
"""
# バイナリ値 (0 or 1) を返す。
evaluator = AspectCritic(
    name="relevance_score",
    definition=definition,
    llm=LangchainLLMWrapper(llm),
)
score = evaluator.single_turn_score(sample)
print(f"Relevance Score: {score}")
