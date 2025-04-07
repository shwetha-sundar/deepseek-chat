import streamlit as st
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import re

# session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

def get_response(messages: list) -> str:
    try:
        endpoint = st.secrets["endpoint"]
        model_name = st.secrets["model_name"]
        token = st.secrets["token"]

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        response = client.complete(
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                *messages
            ],
            max_tokens=1000,
            model=model_name
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return ""

def extract_think_content(response):
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, response, re.DOTALL)
    
    if think_match:
        think_content = think_match.group(1).strip()
        main_response = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        return think_content, main_response
    return None, response

def main():
    st.title('🐳💬 DeepSeek R1 Chatbot')

    with st.sidebar:
        st.header("📚 User Guide")
        st.markdown("""
        ### How to Use
        1. **Start Chatting**: Type your message in the input box at the bottom of the chat
        2. **Continue Conversation**: The chatbot remembers your conversation, so you can ask follow-up questions
        3. **View History**: Scroll up to see your chat history
        4. **Reset Chat**: If you encounter any issues, try resetting the chat using the button below.
        """)

        if st.button("Reset Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hello! How can I help you today?"}
            ]
            st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(st.session_state.messages)
                if response:
                    think_content, main_response = extract_think_content(response)
                    if think_content:
                        st.write(think_content)
                    
                    st.markdown(main_response)
                    st.session_state.messages.append({"role": "assistant", "content": main_response})


if __name__ == "__main__":
    main()