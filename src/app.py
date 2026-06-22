import streamlit as st 
from openai import OpenAI
from google import genai

from core.config import config


def run_llm(provider, model_name, messages, max_tokens=500):

    if provider == "OpenAI":
        client = OpenAI(api_key=config.OPENAI_API_KEY)
    elif provider == "DeepSeek":
        client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL
        )
    else:
        client = genai.Client(api_key=config.GOOGLE_API_KEY)
    
    if provider == "Google":
        return client.models.generate_content(
            model=model_name,
            contents=[message["content"] for message in messages],
        ).text
    elif provider == "DeepSeek":
        return client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_completion_tokens=max_tokens,
            reasoning_effort="low"
        ).choices[0].message.content
    else:
        return client.responses.create(
            model=model_name,
            input=messages,
            max_output_tokens=max_tokens,
            reasoning={
                "effort": "low"  
            }
        ).output_text


with st.sidebar:
    st.title("Settings")

    provider = st.selectbox("Provider", ["OpenAI", "DeepSeek", "Google"])
    if provider == "OpenAI":
        model_name = st.selectbox("Model", [config.OPENAI_MODEL])
    elif provider == "DeepSeek":
        model_name = st.selectbox("Model", [config.DEEPSEEK_MODEL])
    else:
        model_name = st.selectbox("Model", [config.GEMINI_MODEL])

    st.session_state.provider = provider
    st.session_state.model_name = model_name


if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hello! How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = run_llm(st.session_state.provider, st.session_state.model_name, st.session_state.messages)
        response_data = output
        answer = response_data
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
