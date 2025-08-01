import streamlit as st
import os
from components.rag_pipeline import embed_pdf_and_save

def get_course_path(course_id):
    return os.path.join("data", "courses", course_id)

def show_instructor_upload():
    st.title("📥 교안 업로드 및 학습")
    st.markdown("선택된 과정에 교안 PDF를 업로드하고 벡터화를 진행하세요.")

    # 세션 상태 검사
    if "course_id" not in st.session_state or "course_name" not in st.session_state:
        st.warning("⚠️ 먼저 과정을 선택해주세요.")
        return

    course_id = st.session_state["course_id"]
    course_name = st.session_state["course_name"]
    st.markdown(f"📚 선택된 과정: **{course_name}**")

    uploaded_file = st.file_uploader("📎 PDF 교안 업로드", type="pdf")

    if uploaded_file:
        # 저장 경로 설정
        course_path = get_course_path(course_id)
        raw_dir = os.path.join(course_path, "raw")
        os.makedirs(raw_dir, exist_ok=True)

        # ⬇️ 파일 이름을 고정: course_id.pdf
        pdf_filename = f"{course_id}.pdf"
        pdf_path = os.path.join(raw_dir, pdf_filename)

        # 기존 파일 삭제 (선택 사항)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        # 파일 저장
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"✅ PDF 저장 완료: {pdf_path}")            

        # 벡터화 실행
        with st.spinner("🔄 벡터 임베딩 생성 중..."):
            success, message = embed_pdf_and_save(course_id, pdf_path)
            if success:
                st.success(message)
            else:
                st.error("❌ 벡터화 실패")