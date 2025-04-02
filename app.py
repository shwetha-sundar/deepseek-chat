import streamlit as st
from openai import OpenAI

# session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

api_key = st.secrets["api_key"]


def deepseek_chat(api_key: str, messages: list) -> str:
    try:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                *messages
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        return ""


def main():
    st.title('🤖 DeepSeek Chatbot')

    with st.sidebar:
        st.header("📚 User Guide")
        st.markdown("""
        ### How to Use
        1. **Start Chatting**: Type your message in the input box at the bottom of the chat
        2. **Continue Conversation**: The chatbot remembers your conversation, so you can ask follow-up questions
        3. **View History**: Scroll up to see your chat history
        
        ### Tips
        - Be specific with your questions
        - Ask follow-up questions for clarification
        - Use the reset button to start a fresh conversation
        
        ### Need Help?
        If you encounter any issues, try resetting the chat using the button below.
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
                response = deepseek_chat(api_key, st.session_state.messages)
                if response:
                    st.write(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()