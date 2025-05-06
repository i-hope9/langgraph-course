from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_aws import ChatBedrock

llm = ChatBedrock(temperature=0, model="anthropic.claude-3-5-haiku-20241022-v1:0", region="us-west-2")
prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()