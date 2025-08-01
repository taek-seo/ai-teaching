import json
import os

COURSE_INDEX_PATH = "data/metadata/course_index.json"

def load_course_list():
    with open(COURSE_INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_course_by_id(course_id):
    courses = load_course_list()
    return next((c for c in courses if c["course_id"] == course_id), None)

def get_course_path(course_id):
    return f"data/courses/{course_id}/"