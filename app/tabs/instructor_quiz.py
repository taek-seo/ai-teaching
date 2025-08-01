import streamlit as st
import os
import json
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from components.quiz_generator import generate_quiz_batch_from_docs, save_quiz

def show_instructor_quiz():
    st.title("📝 퀴즈 생성기")
    st.markdown("선택한 교안 전체를 기반으로 객관식 퀴즈를 자동 생성합니다.")

    course_id = st.session_state.get("course_id")
    course_name = st.session_state.get("course_name")

    if not course_id:
        st.warning("⚠️ 먼저 과정을 선택해주세요.")
        return

    st.success(f"📘 선택된 과정: {course_name}")

    # 퀴즈 개수 지정
    num_questions = st.slider("생성할 퀴즈 개수", min_value=1, max_value=20, value=5)

    # PDF 원본 경로
    pdf_path = f"data/courses/{course_id}/raw/{course_id}.pdf"
    if not os.path.exists(pdf_path):
        st.error("❌ 교안 PDF 파일이 존재하지 않습니다. 업로드 후 다시 시도해주세요.")
        return

    if st.button("🚀 퀴즈 자동 생성"):
        with st.spinner("🔄 문서 분석 및 퀴즈 생성 중..."):
            loader = PyMuPDFLoader(pdf_path)
            documents = loader.load()
            quizzes = generate_quiz_batch_from_docs(documents, num_questions=num_questions)

        if not quizzes:
            st.error("❌ 퀴즈 생성에 실패했습니다.")
            return

        st.subheader("📋 생성된 퀴즈 미리보기")
        for idx, q in enumerate(quizzes, 1):
            st.markdown(f"**{idx}. {q['question']}**")
            for key, val in q["choices"].items():
                st.markdown(f"- {key}. {val}") 
            st.markdown(f"✅ **정답:** {q['answer']}")
            st.markdown("---")

        if st.button("💾 퀴즈 저장하기"):
            for quiz in quizzes:
                save_quiz(course_id, quiz)
            st.success(f"✅ {len(quizzes)}개의 퀴즈가 저장되었습니다.")
