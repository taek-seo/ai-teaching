import os
import json

COURSE_INDEX_PATH = "data/course_index.json"

def ensure_index_file_exists():
    """파일이 없으면 빈 리스트로 생성"""
    os.makedirs(os.path.dirname(COURSE_INDEX_PATH), exist_ok=True)
    if not os.path.exists(COURSE_INDEX_PATH):
        with open(COURSE_INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

def load_course_index():
    if not os.path.exists(COURSE_INDEX_PATH):
        return []

    try:
        with open(COURSE_INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # 파일이 손상된 경우 빈 리스트로 대체
        return []

def save_course_index(course_list):
    with open(COURSE_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(course_list, f, indent=2, ensure_ascii=False)

def add_course_to_index(course_id, course_name, description, owner_id=None):
    courses = load_course_index()

    # 중복 방지
    if any(c["course_id"] == course_id for c in courses):
        return False, f"⚠️ 이미 등록된 과정 ID입니다: `{course_id}`"

    new_course = {
        "course_id": course_id,
        "course_name": course_name,
        "description": description,
    }
    if owner_id:
        new_course["owner"] = owner_id

    courses.append(new_course)
    save_course_index(courses)

    return True, f"✅ '{course_name}' 과정이 등록되었습니다."