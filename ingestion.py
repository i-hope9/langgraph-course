from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_aws.embeddings.bedrock import BedrockEmbeddings

load_dotenv()

urls = [
     "https://lilianweng.github.io/posts/2023-06-23-agent/",
     "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
     "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
 ]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size = 250, chunk_overlap = 0
)

embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0", region_name="us-west-2"
    )

dot_splits = text_splitter.split_documents(docs_list)
# Chroma: 기본적으로 로컬 PC에 벡터 데이터를 저장하는 벡터 데이터베이스
# 한번 생성에 성공했으니 주석 처리
# vectorstore = Chroma.from_documents(
#     documents=dot_splits,
#     collection_name="rag-chroma",
#     embedding=embeddings,
#     persist_directory="./.chroma"
# )

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=embeddings
).as_retriever()
