import os
import json
import re
from typing import List
from uuid import uuid4
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def generate_mcq_from_text(text: str, num_choices: int = 4) -> dict:
    prompt = f"""
    다음 문단을 읽고, 문단 내용을 바탕으로 하나의 객관식 문제를 생성하세요.

    문단:
    {text}

    아래 형식에 따라 한국어로 출력하세요:
    문제: ...
    보기:
    - A. ...
    - B. ...
    - C. ...
    - D. ...
    정답: (정답 문항 예: A)
    """

    llm = ChatOpenAI(temperature=0.7)
    response = llm.invoke(prompt)

    return parse_mcq_response(response.content)

def parse_mcq_response(response: str) -> dict:
    lines = response.strip().split("\n")
    question = ""
    choices = {}
    answer = ""

    parsing_choices = False

    for line in lines:
        line = line.strip()
        if line.startswith("문제:"):
            question = line.replace("문제:", "").strip()
        elif line.startswith("보기:"):
            parsing_choices = True
        elif re.match(r"- [A-Da-d]\.", line):
            parsing_choices = True
            label = line[2:3].upper()
            content = line[4:].strip()
            choices[label] = content
        elif parsing_choices and re.match(r"[A-Da-d]\.", line):  # 예: "A. 내용"
            label = line[0].upper()
            content = line[2:].strip()
            choices[label] = content
        elif line.startswith("정답:") or line.startswith("답:") or line.lower().startswith("answer:"):
            answer = line.split(":")[-1].strip().upper()

    return {
        "question": question,
        "choices": choices,
        "answer": answer
    }

def evenly_sample_chunks(chunks: List[Document], n: int) -> List[Document]:
    total = len(chunks)
    if n >= total:
        return chunks
    step = total // n
    return [chunks[i * step] for i in range(n)]

def generate_quiz_batch_from_docs(docs: List[Document], num_questions: int = 5) -> List[dict]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    selected_chunks = evenly_sample_chunks(chunks, num_questions)

    quizzes = []
    for chunk in selected_chunks:
        quiz = generate_mcq_from_text(chunk.page_content)
        if quiz:
            quizzes.append(quiz)

    return quizzes

def save_quiz(course_id: str, quiz_data: dict):
    quiz_dir = f"data/courses/{course_id}/quiz"
    os.makedirs(quiz_dir, exist_ok=True)

    # 고유 파일명으로 저장
    filename = f"q_{uuid4().hex}.json"
    filepath = os.path.join(quiz_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)
