from dotenv import load_dotenv

load_dotenv()

from graph.graph import app

if __name__ == '__main__':
    print("hello advanced rag!")
    # Tavily 서치 없이 답변 가능한 경우 
    # print(app.invoke(input={"question": "what is agent memory?"}))

    # Tavily 서치가 필요한 경우
    print(app.invoke(input={"question": "How to make apple pie?"}))