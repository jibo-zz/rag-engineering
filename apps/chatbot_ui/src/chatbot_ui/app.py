import streamlit as st
import requests
from chatbot_ui.core.config import config


def api_call(method, url, **kwargs):
    
    def _show_error_popup(message):
        """Show error message as a popup in the top-right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }
    
    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid JSON response from the server."}
        
        if response.ok:
            return True, response_data
        
        return False, response_data

    except requests.exceptions.ConnectionError:
        _show_error_popup("Failed to connect to the server. Please check your network connection.")
        return False, {"message": "Connection error."}
    except requests.exceptions.Timeout:
        _show_error_popup("The request timed out. Please try again later.")
        return False, {"message": "Request timed out."}
    except Exception as e:
        _show_error_popup(f"An unexpected error occurred: {str(e)}")
        return False, {"message": f"Unexpected error: {str(e)}"}

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

if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        success, response_data = api_call(
            "post",
            f"{config.API_URL}/chat",
            json={
                "provider": st.session_state.provider,
                "model_name": st.session_state.model_name,
                "messages": st.session_state.messages,
            },
        )

        answer = response_data["message"] if success else response_data.get("message", "API error.")
        st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})