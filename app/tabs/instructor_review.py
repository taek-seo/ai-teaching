import os
import streamlit as st
from components.summary_report import (
    generate_report_from_pdf,
    save_text_as_html,
    convert_html_to_pdf,
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def show_instructor_review():
    st.title("📄 복습 자료 생성")
    st.markdown("선택된 과정의 교안을 요약하여 강사용 HTML 자료를 생성합니다.")

    course_id = st.session_state.get("course_id")
    course_name = st.session_state.get("course_name")

    if not course_id:
        st.warning("⚠️ 먼저 과정을 선택해주세요.")
        return

    pdf_path = os.path.join(BASE_DIR, "data", "courses", course_id, "raw", f"{course_id}.pdf")
    if not os.path.exists(pdf_path):
        st.error("❌ 교안 PDF 파일이 존재하지 않습니다. 업로드 후 다시 시도하세요.")
        return

    if st.button("🚀 복습 자료 생성"):
        progress_bar = st.progress(0.0)
        status_area = st.empty()

        def progress(step: int, total: int, message: str) -> None:
            progress_bar.progress(step / total)
            status_area.write(message)

        report_text = generate_report_from_pdf(pdf_path, progress_callback=progress)
        output_dir = os.path.join(BASE_DIR, "data", "courses", course_id)
        html_file = os.path.join(output_dir, "review.html")
        pdf_file = os.path.join(output_dir, "review.pdf")
        save_text_as_html(report_text, html_file)
        convert_html_to_pdf(html_file, pdf_file)

        status_area.write("완료")
        st.success("✅ 복습 자료가 생성되었습니다.")
        with open(html_file, "rb") as f:
            st.download_button("📥 HTML 다운로드", f, file_name=f"{course_id}_review.html")
        with open(pdf_file, "rb") as f:
            st.download_button("📥 PDF 다운로드", f, file_name=f"{course_id}_review.pdf")
