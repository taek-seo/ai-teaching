import os
import sys
import types

# Ensure the project root is in sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Provide a dummy langchain_openai module if not installed
if 'langchain_openai' not in sys.modules:
    dummy = types.ModuleType('langchain_openai')
    dummy.ChatOpenAI = object
    sys.modules['langchain_openai'] = dummy

from app.components.quiz_generator import parse_mcq_response


def test_parse_typical_format():
    resp = (
        "문제: 한국의 수도는 어디인가요?\n"
        "보기:\n"
        "- A. 부산\n"
        "- B. 서울\n"
        "- C. 인천\n"
        "- D. 대구\n"
        "정답: B"
    )
    result = parse_mcq_response(resp)
    assert result['question'] == '한국의 수도는 어디인가요?'
    assert result['choices'] == {'A': '부산', 'B': '서울', 'C': '인천', 'D': '대구'}
    assert result['answer'] == 'B'


def test_parse_without_hyphen_choices():
    resp = (
        "문제: 파이썬의 창시자는 누구인가요?\n"
        "보기:\n"
        "A. 제임스 고슬링\n"
        "B. 귀도 반 로섬\n"
        "C. 데니스 리치\n"
        "D. 켄 톰프슨\n"
        "정답: B"
    )
    result = parse_mcq_response(resp)
    assert result['choices']['B'] == '귀도 반 로섬'
    assert result['answer'] == 'B'


def test_parse_hyphen_without_intro():
    resp = (
        "문제: 2의 제곱은?\n"
        "- A. 3\n"
        "- B. 4\n"
        "- C. 5\n"
        "정답: B"
    )
    result = parse_mcq_response(resp)
    assert result['choices'] == {'A': '3', 'B': '4', 'C': '5'}
    assert result['answer'] == 'B'


def test_parse_answer_variations():
    resp = (
        "문제: 가장 큰 행성은 무엇인가요?\n"
        "보기:\n"
        "- A. 지구\n"
        "- B. 목성\n"
        "- C. 화성\n"
        "답: B"
    )
    result = parse_mcq_response(resp)
    assert result['choices']['B'] == '목성'
    assert result['answer'] == 'B'

    resp2 = (
        "문제: 가장 가까운 별은?\n"
        "보기:\n"
        "- A. 프로키시마\n"
        "- B. 시리우스\n"
        "answer: a"
    )
    result2 = parse_mcq_response(resp2)
    assert result2['answer'] == 'A'

