import streamlit as st
import json
import os
import re
import uuid
from components.course_index_manager import add_course_to_index

COURSE_INDEX_PATH = "data/course_index.json"


# ✅ course_id 자동 생성 (slug + fallback uuid)
def generate_course_id(name: str) -> str:
    slug = re.sub(r"[^\w\sㄱ-힣]", "", name)  # 한글, 영문, 숫자만
    slug = re.sub(r"\s+", "_", slug.strip())
    return slug.lower() if slug else f"course_{uuid.uuid4().hex[:6]}"


# ✅ course_index.json 로드
def load_course_index():
    if not os.path.exists(COURSE_INDEX_PATH):
        return []
    try:
        with open(COURSE_INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


# ✅ 강사용 홈 탭 UI
def show_instructor_home():
    st.title("📂 강사 홈")
    st.markdown("강의 과정을 등록하거나 기존 과정 중 하나를 선택하세요.")

    # === 신규 과정 등록 ===
    st.header("➕ 새 과정 등록")
    with st.form("course_form"):
        name = st.text_input("과정명")
        description = st.text_area("과정 설명")
        submitted = st.form_submit_button("과정 등록하기")

        if submitted:
            if not name:
                st.warning("⚠️ 과정명을 입력해주세요.")
            else:
                course_id = generate_course_id(name)
                new_course = {
                    "course_id": course_id,
                    "course_name": name,
                    "description": description,
                    "owner": st.session_state.get("user_id", "unknown")
                }
                # ✅ 수정된 부분
                success, message = add_course_to_index(
                    new_course["course_id"],
                    new_course["course_name"],
                    new_course["description"],
                    new_course.get("owner")
                )

                if success:
                    st.success(f"✅ '{name}' 과정이 등록되었습니다.")
                    st.session_state["course_id"] = course_id
                    st.session_state["course_name"] = name
                    st.rerun()
                else:
                    st.error(f"❌ 과정 등록 실패: {message}")

    # === 기존 과정 선택 ===
    st.header("📘 등록된 과정 목록")
    course_list = load_course_index()
    valid_courses = [c for c in course_list if isinstance(c, dict) and "course_name" in c and "course_id" in c]

    if not valid_courses:
        st.info("등록된 과정이 없습니다.")
    else:
        selected = st.selectbox("✅ 사용할 과정 선택", options=valid_courses, format_func=lambda c: c["course_name"])

        if st.button("✔️ 선택한 과정으로 설정"):
            st.session_state["course_id"] = selected["course_id"]
            st.session_state["course_name"] = selected["course_name"]
            st.success(f"📌 '{selected['course_name']}' 과정이 선택되었습니다.")
            st.rerun()