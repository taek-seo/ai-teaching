import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pickle

# 데이터 디렉터리 절대 경로
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def embed_pdf_and_save(course_id: str, pdf_path: str):
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectordb = FAISS.from_documents(split_docs, embedding=embeddings)

    save_dir = os.path.join(BASE_DIR, "data", "courses", course_id, "index")
    os.makedirs(save_dir, exist_ok=True)
    vectordb.save_local(save_dir)

    return True, f"✅ 벡터 저장소가 생성되었습니다: {save_dir}"

def qa_from_course(course_id, question):
    """
    업로드된 교안 벡터를 바탕으로 질의응답 수행
    """
    vector_path = os.path.join(BASE_DIR, "data", "courses", course_id, "index")

    if not os.path.exists(vector_path):
        return "❌ 해당 과정의 벡터 데이터가 존재하지 않습니다.", []

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.load_local(vector_path, embeddings, allow_dangerous_deserialization=True)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        verbose=False,
    )

    result = qa_chain({"query": question})
    return result["result"], result.get("source_documents", [])