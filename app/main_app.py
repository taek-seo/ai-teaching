import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from login import login
from router import route_user

def main():
    st.set_page_config(page_title="AI 보조강사", layout="wide")

    # 로그인 세션 확인
    if "user_id" not in st.session_state or "role" not in st.session_state:
        login()
    else:
        st.sidebar.success(f"🧑‍🏫 로그인됨: {st.session_state['user_id']} ({st.session_state['role']})")
        route_user()

if __name__ == "__main__":
    main()