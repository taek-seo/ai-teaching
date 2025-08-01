import json
import os

# 데이터 디렉터리 절대 경로
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
COURSE_INDEX_PATH = os.path.join(BASE_DIR, "data", "course_index.json")

def load_course_list():
    with open(COURSE_INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_course_by_id(course_id):
    courses = load_course_list()
    return next((c for c in courses if c["course_id"] == course_id), None)

def get_course_path(course_id):
    return os.path.join(BASE_DIR, "data", "courses", course_id)