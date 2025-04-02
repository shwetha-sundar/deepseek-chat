import streamlit as st
import chat

st.title("Deep Seek Web Chatbot")
st.write("This is a simple chatbot that demonstrates the use of Azure OpenAI's Chat Completions API.")
st.write("You can ask any question related to the topic of your choice, and the chatbot will respond accordingly.")

query = st.text_area("Enter your question here:")

full_response = ""

if st.button("Submit"):
    with st.spinner("Generating response..."):
        response_container = st.empty()
        for update in chat.get_response(query):
            if update.choices and update.choices[0].delta and update.choices[0].delta.content:
                full_response += update.choices[0].delta.content
                response_container.markdown(full_response)

        chat.client.close()