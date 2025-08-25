# ai-teaching

Streamlit 앱으로 강사와 교육생을 위한 AI 보조 도구를 제공합니다. 교안 업로드 후 질문 응답, 퀴즈 생성 등을 수행할 수 있습니다.

## 새 기능: 복습 자료 PDF 생성
강사는 업로드한 교안을 기반으로 요약 보고서를 생성하여 PDF로 다운로드할 수 있습니다. 사이드바에서 **📄 복습 자료** 탭을 선택하고 버튼을 누르면 OpenAI API를 활용하여 보고서를 작성하고 PDF로 저장합니다.
보고서는 여러 단계의 프롬프트 체이닝으로 생성됩니다. 교안 내용을 요약한 뒤 사전 학습 내용, 전체 요약과 예제, 후속 학습 로드맵, 기술 전망과 참고 자료, 실습 예제를 순차적으로 생성하고 마지막에 종합해 PDF로 내보냅니다.

## 요구 사항
- Python 3.11 이상
- OpenAI API 키 (`OPENAI_API_KEY` 환경 변수)
- `requirements.txt`에 명시된 패키지: Streamlit, LangChain, OpenAI, FAISS, PyMuPDF, pdfkit 등

## 설치 방법
```bash
git clone <repo-url>
cd ai-teaching
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
pip install -r requirements.txt
```
`pdfkit` 사용을 위해 시스템에 `wkhtmltopdf`가 필요할 수 있습니다(Ubuntu: `apt install wkhtmltopdf`).

## 실행 방법
환경 변수 `OPENAI_API_KEY`를 설정한 후 다음 명령을 실행합니다.
```bash
streamlit run app/main_app.py
```

## 폴더 구조
```
app/             Streamlit 앱 소스
  components/   핵심 기능 모듈
  tabs/         역할별 탭 화면
tests/          단위 테스트
requirements.txt 의존성 목록
docs/overview.md 상세 설명 자료
```

## 참고
전체 코드 구조와 모듈 설명은 [docs/overview.md](docs/overview.md)를 참고하세요.
