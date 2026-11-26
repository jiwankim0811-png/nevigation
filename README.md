# Dijkstra Navigation Graph Visualizer (`nevigation`)

다익스트라 알고리즘의 동작 과정을 직관적인 시각화 및 실시간 히스토그램 스냅샷, 시간 복잡도($O((V + E) \log V)$) 분석 메트릭과 함께 제공하는 웹 애플리케이션입니다.

---

## 📁 Repository Structure

```text
nevigation/
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

## 🔒 보안 및 설정 점검

### 1. `.gitignore`
- `.env`, `.env.*`, `*.env` 가 철저하게 등록되어 환경 변수 및 Google Gemini API Key가 저장소에 절대 노출되지 않도록 설정되었습니다.
- `.clasprc.json`, `node_modules/`, `algorithm-class-env/`, `*.log`, `__pycache__/` 등이 배제되어 있습니다.

### 2. `fasion/server/Dockerfile`
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8080
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```
- Cloud Run 호환 포트(`8080`) 및 `PORT` 환경 변수를 지원하도록 설계되었습니다.

---

## 🚀 주요 기능

1. **다익스트라 알고리즘 실시간 탐색 시각화**
   - 수도권 남부 거점(강남역, 양재역, 판교역, 테크노밸리 등) 노드 간 최단 경로 탐색.
   - 거리(km) 및 소요 시간(분) 가중치 전환 지원.

2. **단계별 히스토그램(Histogram) 데이터 생성**
   - 탐색 매 스텝마다 최단거리 구간별 빈도수 및 노드별 확정 상태 스냅샷 반환.

3. **시간 복잡도 & 연산 지연시간 메타데이터**
   - 이론적 복잡도: $O((V + E) \log V)$
   - 누적 연산 수(ops), 간선 이완(relaxation) 성공 횟수, 단계별 마이크로초($\mu s$) 단위 지연시간 실시간 표기.

4. **우선순위 큐(Min-Heap) 리본 & 의사코드 터미널**
   - `[Node, Dist, Prev]` 힙 추출/삽입 시각화 및 실행 라인 하이라이트.

---

## 🌐 Google Apps Script 웹앱 실행 URL

- **`nevigation_graph` 배포 URL**:
  - `https://script.google.com/macros/s/AKfycbz7J-1WxY0j34dV4HQiRnSCozMrmC8rTgXCq_QnFUEJ_8sg0tyLn_rJ1g_MLjXk4U-p6w/exec`
- **`gas` 배포 URL**:
  - `https://script.google.com/macros/s/AKfycbxAKfCDe-OO3dPwfQSq6nfEsOHgRs5RQ-q-FFFXPWNJ9WX7yJ0j6dzQKAKjRNi9i6Y-LQ/exec`
