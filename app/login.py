import streamlit as st

def login():
    st.title("🔐 AI 보조강사 로그인")
    st.markdown("직업훈련 강사 또는 교육생으로 로그인하세요.")

    with st.form("login_form"):
        user_id = st.text_input("사용자 ID 또는 이메일", key="login_user")
        role = st.selectbox("역할 선택", ["👩‍🏫 강사", "👨‍🎓 교육생"], key="login_role")
        submitted = st.form_submit_button("로그인")

    if submitted:
        if not user_id:
            st.warning("❗ 사용자 ID를 입력해주세요.")
            return

        # 세션 상태 저장
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.session_state.role = "instructor" if "강사" in role else "student"

        st.success(f"{role}로 로그인하셨습니다.")
        st.rerun()  