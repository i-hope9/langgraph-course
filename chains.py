from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_aws import ChatBedrock

# 모든 프롬프트와 체인을 정의

# 비평가 역할(생성된 트윗을 보고 피드백. 어떻게 개선할 수 있을지 제안)
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),  # 과거 메시지들 — 우리 에이전트가 참고하고, 비평하고, 반복적으로 개선하는 데 사용할 내용
    ]
)

# 피드백을 바탕으로 트윗을 반복 수정해서 궁극적으로 완벽한 트윗을 만들어냄
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

llm = ChatBedrock(temperature=0, model="anthropic.claude-3-5-haiku-20241022-v1:0", region="us-west-2")
   
generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
