# -
림버스의 거울던전을 더욱 재미있게.우당탕탕 랜덤 덱 생성기.
# 림버스 컴퍼니 인격 랜덤 추첨기

Python의 `random`과 `streamlit`을 사용한 랜덤 웹앱 과제입니다.

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 기능

- 전체 또는 출혈·화상·파열·침잠·진동·호흡·충전 키워드별 추첨
- 1~12명 중 추첨 인원 선택
- 한 번의 덱에서 수감자 중복 방지
- 인격 이름과 등급을 직접 추가
- 결과를 텍스트로 복사하거나 `.txt` 파일로 다운로드
- 등록된 초기 인격 데이터 확인 및 초기화

## GitHub 및 Streamlit Cloud 배포

1. GitHub에서 `random-app` 저장소를 만듭니다.
2. `app.py`와 `requirements.txt`를 저장소 최상위에 업로드하고 커밋합니다.
3. Streamlit Community Cloud에서 GitHub 계정으로 로그인합니다.
4. 새 앱을 만들고 저장소, `main` 브랜치, 메인 파일 경로 `app.py`를 선택합니다.
5. Deploy를 눌러 배포합니다.

참고: 초기 인격 목록은 편집 가능한 참고용 데이터이며, 게임 내 최신 인격과 키워드 분류를 모두 검증한 공식 데이터는 아닙니다.
