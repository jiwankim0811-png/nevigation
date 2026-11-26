# Dijkstra Navigation Graph Visualizer (`nevigation`)

다익스트라 알고리즘의 동작 과정을 직관적인 시각화 및 실시간 히스토그램 스냅샷, 시간 복잡도($O((V + E) \log V)$) 분석 메트릭과 함께 제공하는 풀스택 웹 애플리케이션입니다.

---

## 🌐 실시간 배포 서비스 엔드포인트

| 서비스 구분 | 호스팅 플랫폼 | 상태 | 엔드포인트 URL |
|---|---|:---:|---|
| **백엔드 API 서버 (FastAPI)** | Google Cloud Run (`us-central1`) | 🟢 `Active (200 OK)` | [https://nevigation-server-epaw6mtefq-uc.a.run.app](https://nevigation-server-epaw6mtefq-uc.a.run.app) |
| **API 헬스체크** | Google Cloud Run | 🟢 `Healthy` | [https://nevigation-server-epaw6mtefq-uc.a.run.app/health](https://nevigation-server-epaw6mtefq-uc.a.run.app/health) |
| **시뮬레이터 웹앱 (`nevigation_graph`)** | Google Apps Script (`@3`) | 🟢 `Live` | [https://script.google.com/macros/s/AKfycbzWhm_WRL1OM7INsDg9LezU9tiZZKCkEkRuvQdFzX1L7Wz9ftHnzhl-0OFmXkmK5Et6/exec](https://script.google.com/macros/s/AKfycbzWhm_WRL1OM7INsDg9LezU9tiZZKCkEkRuvQdFzX1L7Wz9ftHnzhl-0OFmXkmK5Et6/exec) |
| **시뮬레이터 웹앱 (`gas`)** | Google Apps Script (`@4`) | 🟢 `Live` | [https://script.google.com/macros/s/AKfycbwt8G-wGQJSFTz3yl6L5TP_0EPgoBX0Jx9FGItCPHmDD9D9vMiWZP5h3Q38ebLK8tiLMQ/exec](https://script.google.com/macros/s/AKfycbwt8G-wGQJSFTz3yl6L5TP_0EPgoBX0Jx9FGItCPHmDD9D9vMiWZP5h3Q38ebLK8tiLMQ/exec) |

---

## 📁 Repository Structure

```text
nevigation/
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions Cloud Run CI/CD 파이프라인
├── .gitignore                   # .env 및 민감/임시 파일 철저 격리
├── README.md                    # 프로젝트 문서
├── package.json
├── database/
│   └── 01_schema.sql            # 네비게이션 노드 및 간선 데이터베이스 스키마
├── fasion/                      # 요청에 따른 하위 폴더 구조
│   └── server/                  # 백엔드 서비스 (FastAPI)
│       ├── Dockerfile           # Python 3.11 Slim 기반 컨테이너 빌드 정의
│       ├── requirements.txt     # fastapi, uvicorn, pydantic 등
│       ├── main.py              # 헬스체크 및 라우터 마운트 엔드포인트
│       └── routers/
│           ├── __init__.py
│           └── algorithm.py     # 다익스트라 엔진 & 단계별 히스토그램/메타데이터 생성
├── gas/                         # Google Apps Script 웹 애플리케이션
│   ├── appsscript.json          # GAS 매니페스트
│   ├── Code.js                  # doGet/doPost 및 백엔드 프록시/내장 시뮬레이터
│   ├── index.html               # Stitch UI 디자인 적용 프론트엔드
│   └── DESIGN.md                # Stitch UI 시스템 토큰 명세서
└── nevigation_graph/            # 독립 배포용 GAS 프로젝트
    ├── appsscript.json
    ├── Code.js
    ├── index.html
    └── DESIGN.md
```

---

## 🔒 보안 및 CI/CD 연동

1. **GitHub Secrets 연동:**
   - `GCP_SA_KEY`: Cloud Run 및 Artifact Registry 권한을 보유한 `github-actions-sa` 인증 키
   - `GCP_PROJECT_ID`: `thetime-1`
   - `GEMINI_API_KEY`: Google AI Studio API 키
   - `GAS_WEBHOOK_URL`: 배포 완료 시 GAS로 신규 서비스 URL 자동 전송 웹훅
2. **자동 스모크 테스트 & 자가 치유:**
   - Cloud Run 배포 즉시 `${{ steps.deploy.outputs.url }}/health`로 HTTP `200 OK` 검증.
