from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import streamlit as st

endpoint = st.secrets["endpoint"]
model_name = st.secrets["model_name"]
token = st.secrets["token"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# response = client.complete(
#     messages=[
#         SystemMessage(content="You are a helpful assistant."),
#         UserMessage(content="I am going to Paris, what should I see?")
#     ],
#     max_tokens=1000,
#     model=model_name
# )

# print(response.choices[0].message.content)

def get_response(prompt):
    response = client.complete(
        stream=True,
        messages=[
            UserMessage(content=prompt)
        ],
        max_tokens=1000,
        model=model_name
    )
    return response