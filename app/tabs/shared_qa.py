import streamlit as st
from components.rag_pipeline import qa_from_course

def show_shared_qa():
    st.title("💬 교안 기반 질의응답 (QA)")

    # 과정 선택 확인
    course_id = st.session_state.get("course_id", None)
    course_name = st.session_state.get("course_name", None)

    if not course_id:
        st.warning("⚠️ 먼저 사용할 과정을 선택하세요.")
        return

    st.markdown(f"🔍 **현재 선택된 과정**: `{course_name}`")

    # 사용자 질문 입력
    question = st.text_input("질문을 입력하세요:")
    if question:
        with st.spinner("⏳ 답변을 생성 중입니다..."):
            answer, sources = qa_from_course(course_id, question)
            st.markdown("### ✅ 답변")
            st.write(answer)

            if sources:
                st.markdown("### 📚 참고 문서")
                for i, doc in enumerate(sources):
                    metadata = doc.metadata
                    page = metadata.get("page", "N/A")
                    st.write(f"• [p.{page}] {doc.page_content[:150]}...")