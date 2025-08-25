# 프로젝트 개요

이 저장소는 **Streamlit** 기반의 "AI 보조강사" 앱을 제공합니다. 강사는 교안을 업로드하여 질문 응답, 퀴즈 생성, 복습 자료 PDF 생성 등을 수행할 수 있고 교육생도 교안을 기반으로 질문하거나 복습할 수 있습니다.

## 디렉터리 구조
- `app/` – Streamlit 앱 소스
  - `main_app.py` – 앱 진입점
  - `login.py` – 간단한 로그인 폼
  - `router.py` – 로그인된 사용자의 역할에 따라 탭을 전환
  - `components/` – 핵심 기능 모듈
    - `course_index_manager.py` – 과정 목록 관리 및 선택
    - `course_loader.py` – PDF 업로드 및 파일 시스템 저장
    - `quiz_generator.py` – OpenAI를 이용한 객관식 퀴즈 생성
    - `rag_pipeline.py` – 교안 PDF를 임베딩하고 질의응답을 수행
    - `summary_report.py` – 교안 내용을 여러 단계로 요약하여 PDF 보고서 생성
  - `tabs/` – 각 기능별 Streamlit 탭
    - `shared_qa.py` – 업로드된 교안을 대상으로 한 공통 질의응답
    - `instructor_home.py` / `student_home.py` – 역할별 홈 화면
    - `instructor_upload.py` – 교안 업로드 및 벡터 인덱스 생성
    - `instructor_quiz.py` – 교안 전체에서 객관식 퀴즈 자동 생성
    - `instructor_review.py` / `student_review.py` – 복습 자료 PDF 생성 및 열람
    - `student_quiz.py` – 학습자가 퀴즈를 풀이
- `tests/` – 단위 테스트(`test_quiz_generator.py`)
- `requirements.txt` – Python 패키지 의존성 목록

## 주요 패키지
- **streamlit** – 웹 UI 프레임워크
- **langchain**, **openai** – LLM 호출 및 RAG 파이프라인 구성
- **faiss-cpu** – 벡터 데이터베이스
- **PyMuPDF**, **pdfkit**, **markdown** – PDF 로딩 및 보고서 생성
- 그 외 `requirements.txt` 참조

## 패키지 설치 방법
```bash
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
pip install -r requirements.txt
```
`pdfkit` 사용을 위해 시스템에 `wkhtmltopdf`가 필요할 수 있습니다(Ubuntu: `apt install wkhtmltopdf`).

## 실행 방법
환경 변수 `OPENAI_API_KEY`를 설정한 뒤 다음 명령으로 실행합니다.
```bash
streamlit run app/main_app.py
```
