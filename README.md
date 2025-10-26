
# AD_dweb_regression

Playwright + Python 기반 웹 광고 영역 회귀 테스트 자동화 프로젝트입니다.  
광고 노출 및 클릭 이벤트가 정상적으로 동작하고, DB 로그가 정확히 적재되는지 검증하며, TestRail 연동과 파라미터라이즈를 통해 테스트 효율을 극대화합니다.

---

## 📁 프로젝트 구조

```
AD_dweb_regression/
├── case_data/        # 테스트레일 연동과 파라미터라이즈화를 위한 TC 번호 데이터
├── json/             # 이벤트 노출/클릭 시간과 상품 번호 데이터 (JSON 형식)
├── pom/              # POM 형식의 함수
├── utils/            # 공통 유틸리티 함수
├── .gitignore        # Git 무시 파일
├── Pipfile           # 의존성 관리 파일
├── Pipfile.lock      # 고정된 의존성 버전
├── config.json       # 환경 설정 파일
├── conftest.py       # Pytest 설정 파일
├── state.json        # 로그인 상태 저장 파일
├── test_srp.py       # SRP 테스트 케이스
└── test_vip.py       # VIP 테스트 케이스
```

---

## ⚙️ 기술 스택

- **언어**: Python 3.11
- **자동화 도구**: Playwright  
- **테스트 프레임워크**: Pytest  
- **의존성 관리**: Pipenv  
- **테스트 관리**: TestRail (TC 연동)  
- **데이터 관리**: JSON / POM  

---

## 🚀 설치 및 실행 방법

### 1. 의존성 설치

```bash
pip install pipenv
pipenv install
```

### 2. 테스트 실행

- 전체 테스트 실행
```bash
pipenv run python test_*.py
```

- 단일 테스트 실행 예시
```bash
pipenv run pytest test_srp.py
pipenv run pytest test_vip.py
```

---

## 주요 기능

- 광고 노출 및 클릭 이벤트 자동 검증  
- DB 로그 적재 여부 확인  
- TestRail 연동을 통한 테스트 결과 기록  
- 검색어별 파라미터라이즈 테스트 적용  
- Slack 알림을 통한 테스트 결과 공유  
- 로그인 상태 유지 및 재사용 가능 (state.json 활용)

---

## 향후 개선 사항

- CI/CD 파이프라인 연동 (예: Jenkins, GitHub Actions)  
- 테스트 커버리지 추가 확대  
- 다양한 광고 영역 및 시나리오 테스트 추가  
- DB 검증 자동화 강화

