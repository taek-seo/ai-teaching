import streamlit as st
from tabs.shared_qa import show_shared_qa
from tabs.instructor_home import show_instructor_home
from tabs.instructor_upload import show_instructor_upload
from tabs.student_home import show_student_home
from tabs.instructor_quiz import show_instructor_quiz
from tabs.instructor_review import show_instructor_review

def route_user():
    # 사용자 정보 출력
    st.sidebar.title("📂 사용자 정보")
    st.sidebar.markdown(f"👤 **ID**: `{st.session_state.get('user_id')}`")
    st.sidebar.markdown(f"🧾 **역할**: {'강사' if st.session_state.role == 'instructor' else '교육생'}")

    if st.sidebar.button("🔓 로그아웃"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 공통 탭 (강사/교육생 공통)
    tabs = ["📘 질문 응답"]

    # 역할 기반 탭 추가
    if st.session_state.role == "instructor":
        tabs += ["📂 강사 홈", "📥 교안 업로드", "📝 퀴즈 생성", "📄 복습 자료"]
    elif st.session_state.role == "student":
        tabs += ["📑 교육생 홈"]

    selected = st.sidebar.radio("📌 기능 선택", tabs)

    # 탭 분기 실행
    if selected == "📘 질문 응답":
        show_shared_qa()
    elif selected == "📂 강사 홈":
        show_instructor_home()
    elif selected == "📥 교안 업로드":
        show_instructor_upload()
    elif selected == "📝 퀴즈 생성":
        show_instructor_quiz()
    elif selected == "📄 복습 자료":
        show_instructor_review()
    elif selected == "📑 교육생 홈":
        show_student_home()
