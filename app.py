from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage, UserMessage
import streamlit as st

endpoint = st.secrets["endpoint"]
token = st.secrets["token"]
model_name = st.secrets["model_name"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

response = client.complete(
    messages=[
        UserMessage(content="How many languages are in the world?"),
    ],
    max_tokens=1000,
    model=model_name
)

print(response.choices[0].message.content)
