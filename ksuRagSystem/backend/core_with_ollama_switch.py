import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.schema import Document

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Load .env configuration
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

# Choose between OpenAI and Ollama toggle
USE_OLLAMA = False

# Set up embeddings (OpenAI only for now)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=OPENAI_API_KEY)

# Connect to Pinecone
vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)

# Custom prompt
retrieval_qa_chat_prompt = PromptTemplate(
    input_variables=["input", "context"],
    template="""
    أنت مساعد ذكي مخصص للطلاب في جامعة الملك سعود. مهمتك هي الإجابة بدقة ووضوح على أسئلة الطلاب المتعلقة بما يلي:

    - التواريخ الأكاديمية المهمة (مثل بداية الفصل، فترات التسجيل، الحذف والإضافة، الاختبارات، التخرج).
    - الإجراءات الإدارية والأكاديمية (مثل التحويل بين الكليات، رفع الأعذار، التقديم على التدريب أو التخرج).
    - الأنظمة واللوائح الجامعية.
    - الخدمات الطلابية (مثل السكن، النقل، الدعم الفني، البطاقات الجامعية).
    - أي استفسارات أخرى تتعلق بالحياة الجامعية.
    يجب أن تكون إجابتك باللغة العربية الفصحى فقط، وبلغة واضحة وسهلة الفهم للطالب.
    اعتمد في إجاباتك فقط على المعلومات الموجودة في السياق المقدم لك، ولا تضف أي معلومات من خارج المصدر.

    ---

    السياق:
    {context}

    ---

    سؤال الطالب:
    {input}
    """
)


condense_prompt = PromptTemplate(
    input_variables=["chat_history", "input"],
    template="""
    بناءً على المحادثة السابقة:
    {chat_history}

    وصيغة السؤال الجديد:
    {input}

    أعد صياغة السؤال ليستقل بذاته:
    """
)


# LLM selector
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)


# Chain setup
def get_chain():
    retriever = vectorstore.as_retriever()

    # Use custom condense prompt
    history_aware_retriever = create_history_aware_retriever(
        llm=llm,
        retriever=retriever,
        prompt=condense_prompt
    )

    doc_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, doc_chain)
    return rag_chain



# Inference function
def run_llm(query: str, chat_history: List[Any]) -> Dict[str, Any]:
    chain = get_chain()
    response = chain.invoke({
        "input": query,
        "chat_history": chat_history  # ✅ this is required
    })
    return {"result": response["answer"]}


