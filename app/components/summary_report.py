# summary_report.py
import os
import re
import textwrap
from typing import List

from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fpdf import FPDF

# 프로젝트 루트(BASE_DIR): 이 파일(components/summary_report.py 등) 위치 기준 상위 디렉터리
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# ---------------------------
# PDF -> 텍스트 로딩/요약 파트
# ---------------------------
def load_pdf_text(pdf_path: str) -> str:
    """주어진 PDF 파일의 전체 텍스트를 로드합니다."""
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join(doc.page_content for doc in docs)


def summarize_chunks(text: str, llm: ChatOpenAI, chunk_size: int = 1500, overlap: int = 100) -> str:
    """
    텍스트를 청크로 나눈 뒤 각 청크를 요약하고 결합합니다.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks: List[str] = splitter.split_text(text)
    summaries: List[str] = []

    for chunk in chunks:
        prompt = "다음 교안 내용을 간략히 요약하세요:\n" + chunk
        summaries.append(llm.invoke(prompt).content)

    return "\n".join(summaries)


def generate_report_from_pdf(pdf_path: str, model: str = "gpt-4o-mini", temperature: float = 0.3) -> str:
    """
    과정 PDF를 기반으로 강사용 리뷰 보고서를 섹션별로 생성합니다.
    """
    llm = ChatOpenAI(model=model, temperature=temperature)

    raw_text = load_pdf_text(pdf_path)
    partial_summary = summarize_chunks(raw_text, llm)

    # 1) 사전 학습
    pre_prompt = f"""
다음 교안을 학습하기 전에 필요한 배경 지식과 사전 학습 내용을 자세히 설명하세요.
교안 요약:
{partial_summary}
"""
    pre_learning = llm.invoke(pre_prompt).content

    # 2) 전체 요약 + 예시
    summary_prompt = f"""
교안 전체 내용을 요약하고 각 주요 항목에 대한 간단한 설명과 적절한 예제를 포함해 주세요.
요약:
{partial_summary}
"""
    main_summary = llm.invoke(summary_prompt).content

    # 3) 후순위 로드맵
    roadmap_prompt = f"""
강의 이후 후순위로 학습하면 좋은 주제들을 로드맵 형식으로 정리하세요.
요약:
{partial_summary}
"""
    roadmap = llm.invoke(roadmap_prompt).content

    # 4) 전망/참고
    outlook_prompt = f"""
해당 기술 분야의 전망을 분석하고, 알아두면 좋은 관련 기술과 참고 도서 또는 자료를 추천하세요.
요약:
{partial_summary}
"""
    outlook = llm.invoke(outlook_prompt).content

    # 5) 실습
    practice_prompt = f"""
{partial_summary} 내용을 바탕으로 해보면 좋은 실습 예제 두 개와 간단한 해설을 제시하세요.
"""
    practice = llm.invoke(practice_prompt).content

    # 최종 리뷰/정리
    draft_report = "\n\n".join(
        [
            "### 사전 학습 내용",
            pre_learning,
            "### 전체 내용 요약 및 설명",
            main_summary,
            "### 후순위 학습 로드맵",
            roadmap,
            "### 기술 전망 및 참고 자료",
            outlook,
            "### 실습 예제",
            practice,
        ]
    )

    review_prompt = f"다음 내용을 하나의 보고서 형태로 다듬어 주세요.\n\n{draft_report}"
    final_report = llm.invoke(review_prompt).content
    return final_report


# ---------------------------
# 텍스트 -> PDF 저장 파트
# ---------------------------
def _soft_wrap_long_tokens(s: str, limit: int = 80) -> str:
    """
    공백 없이 너무 긴 연속 토큰(예: URL, 해시)을 적당히 쪼개도록
    소프트 공백을 삽입합니다. (FPDF 줄바꿈 보조)
    """
    return re.sub(r"(\S{" + str(limit) + r"})(?=\S)", r"\1 ", s)


def _wrap_text_line(line: str, char_width: int = 100) -> str:
    """
    문자 기준 래핑. 긴 토큰도 강제로 쪼개도록 설정합니다.
    """
    return textwrap.fill(
        line,
        width=char_width,
        break_long_words=True,
        break_on_hyphens=False,
    )


def _try_set_korean_font(pdf: FPDF) -> None:
    """
    나눔고딕 폰트를 등록하고 설정합니다.
    폰트 파일이 없으면 기본 폰트(Helvetica)로 폴백합니다.
    """
    font_path = os.path.join(BASE_DIR, "assets", "fonts", "NanumGothic-Regular.ttf")
    if os.path.isfile(font_path):
        pdf.add_font("Nanum", "", font_path, uni=True)
        pdf.set_font("Nanum", size=12)
    else:
        # 폴백(영문/숫자 위주 출력은 정상, 한글은 네모로 보일 수 있음)
        pdf.set_font("Helvetica", size=12)


def save_text_as_pdf(text: str, output_path: str) -> None:
    """
    텍스트를 (한글 지원) PDF로 저장합니다.
    - 유효폭(effective_w)을 명시적으로 사용
    - 매 라인마다 set_x(l_margin)로 들여쓰기 초기화
    - 긴 토큰을 소프트 래핑하여 FPDF 줄바꿈 지원
    """
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    # 마진/오토페이지 설정을 먼저 적용
    pdf.set_margins(left=15, top=15, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # 폰트 설정(나눔고딕 또는 폴백)
    _try_set_korean_font(pdf)

    # 유효폭(mm)
    effective_w = pdf.w - pdf.l_margin - pdf.r_margin

    # 줄 간격(mm)
    line_h = 7

    for raw_line in text.split("\n"):
        line = raw_line.strip()

        if not line:
            # 공백 라인: 살짝 여백만
            pdf.ln(line_h - 1)
            continue

        # 공백 없는 긴 토큰을 부드럽게 쪼갠 뒤 전체 래핑
        line = _soft_wrap_long_tokens(line, limit=80)
        wrapped = _wrap_text_line(line, char_width=100)

        # 항상 왼쪽 마진부터 시작
        pdf.set_x(pdf.l_margin)

        # 남은 폭(0)이 아니라 유효폭을 명시적으로 지정
        pdf.multi_cell(w=effective_w, h=line_h, txt=wrapped)

    # 출력 경로 보장 후 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)