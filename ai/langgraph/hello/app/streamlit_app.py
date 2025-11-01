import uuid
from langgraph.types import Command
from langchain_core.messages import HumanMessage
import streamlit as st

from x_agent_core import agent


def init_session_state():
    """セッションの初期化"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "waiting_for_approval" not in st.session_state:
        st.session_state.waiting_for_approval = False
    if "final_result" not in st.session_state:
        st.session_state.final_result = None
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = None


def reset_session():
    """セッションのリセット"""
    st.session_state.messages = []
    st.session_state.waiting_for_approval = False
    st.session_state.final_result = None
    st.session_state.thread_id = None


init_session_state()


def run_agent(input_data):
    config = {
        "configurable": {
            "thread_id": st.session_state.thread_id,
        }
    }

    with st.spinner("処理中。。。", show_time=True):
        for chunk in agent.stream(input_data, stream_mode="updates", config=config):
            for task_name, result in chunk.items():
                # interrupt の場合。
                if task_name == "__interrupt__":
                    st.session_state.tool_info = result[0].value
                    st.session_state.waiting_for_approval = True
                # 最終回答。
                elif task_name == "agent":
                    final_text = result.content
                    if isinstance(final_text, list):
                        # LangChain の AIMessage は list の場合がある。
                        texts = [
                            block.get("text", "")
                            for block in final_text
                            if isinstance(block, dict) and block.get("type") == "text"
                        ]
                        final_text = "\n".join(filter(None, texts))
                    if not isinstance(final_text, str):
                        final_text = str(final_text)
                    st.session_state.final_result = final_text
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": final_text,
                        }
                    )
                # LLM 推論の場合。
                elif task_name == "invoke_llm":
                    # list じゃない場合もある？
                    llm_content = chunk["invoke_llm"].content
                    if isinstance(llm_content, list):
                        for content in result.content:
                            # text じゃない場合ある？
                            if content["type"] == "text":
                                st.session_state.messages.append(
                                    {
                                        "role": "assistant",
                                        "content": content["text"],
                                    }
                                )
                    elif isinstance(llm_content, str):
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": llm_content,
                            }
                        )
                # ツール実行の場合。
                elif task_name == "use_tool":
                    st.session_state.messages.append(
                        {"role": "assistant", "content": "ツールを実行！"}
                    )
        st.rerun()


def feedback():
    approve_column, deny_column = st.columns(2)

    feedback_result = None
    with approve_column:
        if st.button("承認", width="stretch"):
            st.session_state.waiting_for_approval = False
            feedback_result = "APPROVE"
    with deny_column:
        if st.button("拒否", width="stretch"):
            st.session_state.waiting_for_approval = False
            feedback_result = "DENY"
    # いずれかのボタンが押された。
    return feedback_result


def app():
    st.title("Web 検索エージェント with LangGraph")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
            # st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    if st.session_state.waiting_for_approval and st.session_state.tool_info:
        st.info("ツール使用の承認を求めています。" + st.session_state.tool_info["args"])
        if st.session_state.tool_info["name"] == "write_file":
            st.html(
                st.session_state.tool_info["html"],
                width="stretch",
            )
        feedback_result = feedback()
        if feedback_result:
            st.chat_message("user").write(feedback_result)
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": feedback_result,
                }
            )
            run_agent(Command(resume=feedback_result))
            st.rerun()

    if st.session_state.final_result and not st.session_state.waiting_for_approval:
        st.success("エージェントの処理が完了しました。")
        st.success(st.session_state.final_result)

    if not st.session_state.waiting_for_approval:
        user_input = st.chat_input("質問を入力してください。")
        if user_input:
            reset_session()
            st.session_state.thread_id = str(uuid.uuid4())

            st.chat_message("user").write(user_input)
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_input,
                }
            )

            messages = [HumanMessage(content=user_input)]
            if run_agent(messages):
                st.rerun()
    else:
        st.info("ツール使用の承認を待っています。")


if __name__ == "__main__":
    app()
