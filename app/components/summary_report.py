import os
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_pdf_text(pdf_path: str) -> str:
    """Load entire PDF text."""
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    return "\n".join(doc.page_content for doc in docs)


def summarize_chunks(text: str, llm: ChatOpenAI) -> str:
    """Split text and summarize each chunk, then combine."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    chunks = splitter.split_text(text)
    summaries = []
    for chunk in chunks:
        prompt = (
            "다음 교안 내용을 간략히 요약하세요:\n" + chunk
        )
        summaries.append(llm.invoke(prompt).content)
    return "\n".join(summaries)


def generate_report_from_pdf(pdf_path: str) -> str:
    """Create multi-section instructor review report from a course PDF."""
    llm = ChatOpenAI(temperature=0.3)

    raw_text = load_pdf_text(pdf_path)
    partial_summary = summarize_chunks(raw_text, llm)

    # 1) Pre-learning requirements
    pre_prompt = f"""
다음 교안을 학습하기 전에 필요한 배경 지식과 사전 학습 내용을 자세히 설명하세요.
교안 요약:
{partial_summary}
"""
    pre_learning = llm.invoke(pre_prompt).content

    # 2) Main summary with examples
    summary_prompt = f"""
교안 전체 내용을 요약하고 각 주요 항목에 대한 간단한 설명과 적절한 예제를 포함해 주세요.
요약:
{partial_summary}
"""
    main_summary = llm.invoke(summary_prompt).content

    # 3) Follow-up roadmap
    roadmap_prompt = f"""
강의 이후 후순위로 학습하면 좋은 주제들을 로드맵 형식으로 정리하세요.
요약:
{partial_summary}
"""
    roadmap = llm.invoke(roadmap_prompt).content

    # 4) Outlook and references
    outlook_prompt = f"""
해당 기술 분야의 전망을 분석하고, 알아두면 좋은 관련 기술과 참고 도서 또는 자료를 추천하세요.
요약:
{partial_summary}
"""
    outlook = llm.invoke(outlook_prompt).content

    # 5) Practice exercises
    practice_prompt = f"""
{partial_summary} 내용을 바탕으로 해보면 좋은 실습 예제 두 개와 간단한 해설을 제시하세요.
"""
    practice = llm.invoke(practice_prompt).content

    # Combine all sections and ask for a final review
    draft_report = "\n\n".join([
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
    ])

    review_prompt = f"다음 내용을 하나의 보고서 형태로 다듬어 주세요.\n\n{draft_report}"
    final_report = llm.invoke(review_prompt).content
    return final_report


def save_text_as_pdf(text: str, output_path: str) -> None:
    """텍스트를 한글 지원 PDF로 저장"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # ✅ 한글 지원 폰트 등록
    font_path = os.path.join(BASE_DIR, "assets", "fonts", "NanumGothic-Regular.ttf")
    pdf.add_font("Nanum", "", font_path, uni=True)
    pdf.set_font("Nanum", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 10, txt=line)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)