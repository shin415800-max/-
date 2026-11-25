# -*- coding: utf-8 -*-
"""림버스 컴퍼니 인격 랜덤 추첨기 - Streamlit 앱

실행: streamlit run app.py
"""

import copy
import random

import streamlit as st


KEYWORDS = ["출혈", "화상", "파열", "침잠", "진동", "호흡", "충전"]

# 초기 데이터입니다. 인격을 더하거나 수정할 수 있도록 앱 안에 입력 기능을 넣었습니다.
# 일부 목록은 이전 대화에서 정리한 초안이므로, 실제 게임 내 인격/키워드 분류와
# 다를 수 있습니다. 공개 전 게임 내 정보를 기준으로 한 번 더 확인해 주세요.
BASE_IDENTITIES = [
    {
        "sinner": "이상",
        "출혈": ["피쿼드호 일등 항해사", "약지 점묘파 스튜던트", "N사 E.G.O::흉탄"],
        "화상": ["남부 리우 협회 3과"],
        "파열": ["LCE E.G.O::초롱", "남부 세븐 협회 6과", "W사 3등급 정리 요원", "흑수 - 오 필두", "LCE E.G.O::차원찢개"],
        "침잠": ["남부 디에치 협회 4과", "LCB 수감자", "개화 E.G.O::동백", "로보토미 E.G.O::엄숙한 애도", "거미집 검지 아비"],
        "진동": [],
        "호흡": ["피쿼드호 일등 항해사", "검계 살수", "N사 E.G.O::흉탄", "거미집 검지 아비"],
        "충전": ["W사 3등급 정리 요원", "LCE E.G.O::차원찢개"],
    },
    {
        "sinner": "파우스트",
        "출혈": ["쥐는 자", "검계 살수", "동부 시 협회 3과", "거미집 약지 제자"],
        "화상": ["LCE E.G.O::홍염살", "새벽 사무소 해결사"],
        "파열": ["살아남은 로보토미 직원", "남부 세븐 협회 4과", "흑수 - 묘 필두"],
        "침잠": ["워더링하이츠 버틀러", "검지 수행자:【쪽지】"],
        "진동": ["로보토미 E.G.O::후회", "새벽 사무소 해결사"],
        "호흡": ["검계 살수", "동부 시 협회 3과"],
        "충전": ["W사 2등급 정리 요원", "멀티크랙 사무소 대표", "거미집 약지 제자"],
    },
    {
        "sinner": "돈키호테",
        "출혈": ["LCB 수감자", "N사 중간 망치", "중지 작은 아우", "라만차랜드 실장"],
        "화상": ["동부 섕크 협회 3과"],
        "파열": ["로보토미 E.G.O::초롱", "W사 3등급 정리 요원", "로보토미 E.G.O::사랑과 증오의 이름으로", "흑수 - 미"],
        "침잠": ["로보토미 E.G.O::사랑과 증오의 이름으로", "흑수 - 미", "검지 대행자 - 개화 E.G.O::대행"],
        "진동": ["N사 중간 망치", "T사 3등급 징수직 직원", "오트쿠튀르::르누아르 브랜드 매니저", "쐐기 사무소 해결사"],
        "호흡": ["남부 시 협회 5과 부장", "검계 살수", "동부 섕크 협회 3과", "검지 대행자 - 개화 E.G.O::대행", "쐐기 사무소 해결사"],
        "충전": ["W사 3등급 정리 요원", "로보토미 E.G.O::사랑과 증오의 이름으로", "오트쿠튀르::르누아르 브랜드 매니저"],
    },
    {
        "sinner": "료슈",
        "출혈": ["거미집의 검", "N사 E.G.O::경멸, 경외", "로보토미 E.G.O::적안 · 참회", "료.고.파. 주방장", "흑운회 와카슈"],
        "화상": ["거미집의 검", "남부 리우 협회 4과"],
        "파열": ["홍원 방랑무사", "흑수 - 묘", "남부 세븐 협회 6과", "LCCB 대리"],
        "침잠": ["로보토미 E.G.O::잔향 · 외로움"],
        "진동": ["오트쿠튀르::르누아르 신발관", "로보토미 E.G.O::잔향 · 외로움", "N사 E.G.O::경멸, 경외", "LCCB 대리", "20구 유로지비"],
        "호흡": ["거미집의 검", "홍원 방랑무사", "에드가 가문 치프 버틀러", "LCCB 대리"],
        "충전": ["오트쿠튀르::르누아르 신발관", "로보토미 E.G.O::적안 · 참회", "W사 3등급 정리 요원"],
    },
    {
        "sinner": "뫼르소",
        "출혈": ["약지 야수파 스튜던트", "로보토미 E.G.O::호넷〖변조〗", "라만차랜드 왕자", "검계 우두머리", "중지 작은 아우", "R사 제 4무리 코뿔소팀", "N사 큰 망치"],
        "화상": ["로보토미 E.G.O::호넷〖변조〗", "동부 엄지 카포 IIII", "남부 리우 협회 6과"],
        "파열": ["라만차랜드 왕자", "서부 섕크 협회 3과", "데드레빗츠 보스", "W사 2등급 정리 요원"],
        "침잠": ["약지 야수파 스튜던트", "남부 디에치 협회 4과 부장"],
        "진동": ["동부 엄지 카포 IIII", "장미스패너 공방 해결사", "LCB 수감자"],
        "호흡": ["검계 우두머리"],
        "충전": ["R사 제 4무리 코뿔소팀", "W사 2등급 정리 요원", "장미스패너 공방 해결사"],
    },
    {
        "sinner": "홍루",
        "출혈": ["S사 추노꾼", "거미집 약지 아비", "갈고리 사무소 해결사", "흑운회 와카슈", "콩콩이파 두목"],
        "화상": ["동부 섕크 협회 3과", "남부 리우 협회 5과"],
        "파열": ["홍원 군주", "송곳니 사냥 사무소 해결사", "W사 2등급 정리 요원", "K사 3등급 적출직 직원", "LCB 수감자"],
        "침잠": ["R사 제 4무리 순록팀", "남부 디에치 협회 4과", "LCB 수감자"],
        "진동": ["오트쿠튀르::르누아르 3F 방송실", "20구 유로지비"],
        "호흡": ["S사 추노꾼", "홍원 군주", "마침표 사무소 대표"],
        "충전": ["오트쿠튀르::르누아르 3F 방송실", "거미집 약지 아비", "R사 제 4무리 순록팀", "W사 2등급 정리 요원"],
    },
    {
        "sinner": "히스클리프",
        "출혈": ["오트쿠튀르::르루주 바느질의 왕", "중지 작은 형님", "흑운회 와카슈", "피쿼드호 작살잡이", "R사 제 4무리 토끼팀", "N사 작은 망치"],
        "화상": ["거미집 엄지 제자", "중지 작은 형님", "흑수 - 유 필두"],
        "파열": ["W사 4등급 정리 요원 - CCA", "흑수 - 유 필두", "남부 세븐 협회 4과", "로보토미 E.G.O::여우비", "R사 제 4무리 토끼팀"],
        "침잠": ["와일드헌트", "로보토미 E.G.O::여우비"],
        "진동": ["거미집 엄지 제자", "남부 외우피 협회 3과", "LCB 수감자"],
        "호흡": ["피쿼드호 작살잡이", "남부 시 협회 5과"],
        "충전": ["오트쿠튀르::르루주 바느질의 왕", "W사 4등급 정리 요원 - CCA", "멀티크랙 사무소 해결사", "R사 제 4무리 토끼팀"],
    },
    {
        "sinner": "이스마엘",
        "출혈": ["오트쿠튀르::르루주 부티크", "LCD 현장추리팀", "거미집 중지 제자", "피쿼드호 선장", "흑운회 부조장"],
        "화상": ["거미집 중지 제자", "피쿼드호 선장", "남부 리우 협회 4과"],
        "파열": ["가주 후보", "로보토미 E.G.O::출렁임", "LCCB 대리"],
        "침잠": ["정사무소 대표", "에드가 가문 버틀러", "R사 제 4무리 순록팀", "어금니 보트 센터 해결사"],
        "진동": ["정사무소 대표", "서부 츠바이 협회 3과", "로보토미 E.G.O::출렁임", "LCCB 대리", "어금니 보트 센터 해결사", "LCB 수감자"],
        "호흡": ["LCD 현장추리팀", "피쿼드호 선장", "에드가 가문 버틀러"],
        "충전": ["오트쿠튀르::르루주 부티크", "R사 제 4무리 순록팀"],
    },
    {
        "sinner": "로쟈",
        "출혈": ["거미집 엄지 아비", "약지 야수파 도슨트", "라만차랜드 공주", "흑운회 와카슈", "N사 중간 망치"],
        "화상": ["거미집 엄지 아비", "남부 리우 협회 4과 부장"],
        "파열": ["라만차랜드 공주", "흑수 - 사", "북부 제뱌찌 협회 3과"],
        "침잠": ["약지 야수파 도슨트", "R사 제 4무리 순록팀", "로보토미 E.G.O::눈물로 벼려낸 검", "남부 디에치 협회 4과"],
        "진동": ["거미집 엄지 아비", "T사 2등급 징수직 직원", "장미스패너 공방 대표"],
        "호흡": ["흑운회 와카슈", "남부 츠바이 협회 5과"],
        "충전": ["R사 제 4무리 순록팀", "로보토미 E.G.O::눈물로 벼려낸 검", "장미스패너 공방 대표"],
    },
    {
        "sinner": "싱클레어",
        "출혈": ["오트쿠튀르::르루주 붉은 신", "거미집 소지 제자", "중지 작은 아우", "검계 살수", "쥐어들 자"],
        "화상": ["새벽 사무소 해결사", "동부 엄지 솔다토 II", "쥐어들 자", "흑수 - 유"],
        "파열": ["북부 제뱌찌 협회 3과", "남부 섕크 협회 4과 부장", "로보토미 E.G.O::홍적", "LCB 수감자", "흑수 - 유"],
        "침잠": ["마리아치 보스"],
        "진동": ["서부 츠바이 협회 3과", "동부 엄지 솔다토 II", "남부 츠바이 협회 6과", "어금니 보트 센터 해결사"],
        "호흡": ["거미집 소지 제자", "검계 살수", "마리아치 보스", "남부 섕크 협회 4과 부장"],
        "충전": ["오트쿠튀르::르루주 붉은 신"],
    },
    {
        "sinner": "오티스",
        "출혈": ["거미집 중지 아비", "라만차랜드 이발사", "약지 점묘파 스튜던트"],
        "화상": ["거미집 중지 아비", "로보토미 E.G.O::마탄"],
        "파열": ["흑수 - 묘", "W사 3등급 정리 요원 팀장", "남부 세븐 협회 6과 부장", "LCB 수감자"],
        "침잠": ["LCA 우제트 선봉 3팀 팀장", "워더링하이츠 치프 버틀러", "G사 부장"],
        "진동": ["LCA 우제트 선봉 3팀 팀장", "T사 3등급 강력징수직 직원", "어금니 사무소 해결사"],
        "호흡": ["쐐기 사무소 대표", "남부 섕크 협회 4과"],
        "충전": ["W사 3등급 정리 요원 팀장"],
    },
    {
        "sinner": "그레고르",
        "출혈": ["밤의 송곳 카피타노", "라만차랜드 신부", "흑운회 부조장", "쌍갈고리 해적단 부선장", "료.고.파. 조수", "흑수 - 사"],
        "화상": ["새벽 사무소 대표", "로보토미 E.G.O::램프", "불주먹 사무소 생존자", "남부 리우 협회 6과"],
        "파열": ["LCE E.G.O::AEDD", "라만차랜드 신부", "장미스패너 공방 해결사", "G사 일등대리", "LCB 수감자", "흑수 - 사"],
        "침잠": ["로보토미 E.G.O::램프", "에드가 가문 승계자"],
        "진동": ["새벽 사무소 대표", "밤의 송곳 카피타노", "장미스패너 공방 해결사"],
        "호흡": ["쌍갈고리 해적단 부선장", "흑수 - 사"],
        "충전": ["LCE E.G.O::AEDD", "장미스패너 공방 해결사"],
    },
]


def normalize_identity(identity):
    """문자열 또는 {'name': ..., 'rarity': ...} 형식을 통일합니다."""
    if isinstance(identity, str):
        name = identity.strip()
        return {"name": name, "rarity": ""} if name else None
    if isinstance(identity, dict) and identity.get("name"):
        name = str(identity["name"]).strip()
        rarity = str(identity.get("rarity", "")).strip()
        return {"name": name, "rarity": rarity} if name else None
    return None


def build_candidates(identity_data, selected_keyword):
    """키워드별 인격을 모으고, 같은 인격의 중복 등록은 한 번으로 합칩니다."""
    candidates = []
    keywords_to_check = KEYWORDS if selected_keyword == "전체" else [selected_keyword]

    for sinner_data in identity_data:
        collected = {}
        for keyword in keywords_to_check:
            raw_list = sinner_data.get(keyword, [])
            if not isinstance(raw_list, list):
                continue
            for raw_identity in raw_list:
                identity = normalize_identity(raw_identity)
                if identity is None:
                    continue
                key = (identity["name"], identity["rarity"])
                if key not in collected:
                    collected[key] = {
                        **identity,
                        "keywords": [],
                    }
                if keyword not in collected[key]["keywords"]:
                    collected[key]["keywords"].append(keyword)

        identities = list(collected.values())
        if identities:
            candidates.append({
                "sinner": sinner_data["sinner"],
                "identities": identities,
            })
    return candidates


st.set_page_config(
    page_title="인격 랜덤 추첨기",
    page_icon="🎲",
    layout="wide",
)

if "identity_data" not in st.session_state:
    st.session_state.identity_data = copy.deepcopy(BASE_IDENTITIES)
if "current_deck" not in st.session_state:
    st.session_state.current_deck = []

st.title("🎲 림버스 컴퍼니 인격 랜덤 추첨기")
st.caption("수감자와 키워드를 선택해 중복 수감자 없이 무작위 덱을 만들어 보세요.")

with st.sidebar:
    st.header("⚙️ 추첨 설정")
    selected_keyword = st.selectbox("키워드", ["전체"] + KEYWORDS)
    sinner_count = st.slider("추첨할 수감자 수", min_value=1, max_value=12, value=6)

    st.divider()
    st.subheader("인격 추가")
    with st.form("add_identity_form", clear_on_submit=True):
        selected_sinner = st.selectbox(
            "수감자",
            [item["sinner"] for item in st.session_state.identity_data],
        )
        selected_add_keyword = st.selectbox("키워드", KEYWORDS)
        new_identity_name = st.text_input("인격 이름", placeholder="예: 검계 살수")
        new_identity_rarity = st.text_input("등급 (선택)", placeholder="예: 3성")
        add_submitted = st.form_submit_button("인격 목록에 추가", use_container_width=True)

    if add_submitted:
        clean_name = new_identity_name.strip()
        if not clean_name:
            st.warning("인격 이름을 입력해 주세요.")
        else:
            target = next(
                item for item in st.session_state.identity_data
                if item["sinner"] == selected_sinner
            )
            current_items = target.setdefault(selected_add_keyword, [])
            normalized_existing = [normalize_identity(item) for item in current_items]
            is_duplicate = any(
                item and item["name"] == clean_name
                and item["rarity"] == new_identity_rarity.strip()
                for item in normalized_existing
            )
            if is_duplicate:
                st.info("이미 해당 수감자의 키워드 목록에 등록된 인격입니다.")
            else:
                if new_identity_rarity.strip():
                    current_items.append({
                        "name": clean_name,
                        "rarity": new_identity_rarity.strip(),
                    })
                else:
                    current_items.append(clean_name)
                st.success(f"{selected_sinner}의 {selected_add_keyword} 목록에 추가했습니다.")
                st.rerun()

    if st.button("초기 데이터로 되돌리기", use_container_width=True):
        st.session_state.identity_data = copy.deepcopy(BASE_IDENTITIES)
        st.session_state.current_deck = []
        st.rerun()

candidates = build_candidates(st.session_state.identity_data, selected_keyword)
available_count = len(candidates)

metric_col1, metric_col2 = st.columns(2)
metric_col1.metric("등록된 수감자", f"{available_count}명")
metric_col2.metric("추첨 인원", f"{sinner_count}명")

if st.button("✨ 랜덤 덱 생성", type="primary", use_container_width=True):
    if available_count < sinner_count:
        st.session_state.current_deck = []
        st.error(
            f"'{selected_keyword}' 키워드에 등록된 수감자는 {available_count}명입니다. "
            f"추첨 인원을 줄이거나 인격을 더 추가해 주세요."
        )
    else:
        # random.sample()로 서로 다른 수감자를 뽑고, random.choice()로 각 수감자의 인격을 고릅니다.
        selected_sinners = random.sample(candidates, k=sinner_count)
        new_deck = []
        for sinner in selected_sinners:
            identity = random.choice(sinner["identities"])
            new_deck.append({
                "sinner": sinner["sinner"],
                "name": identity["name"],
                "rarity": identity["rarity"],
                "keywords": identity["keywords"],
            })
        st.session_state.current_deck = new_deck

st.divider()
st.subheader("📜 추첨 결과")

if st.session_state.current_deck:
    deck = st.session_state.current_deck
    columns = st.columns(3)
    for index, entry in enumerate(deck):
        with columns[index % 3]:
            with st.container(border=True):
                st.caption(f"NO. {index + 1:02d}")
                st.markdown(f"### {entry['sinner']}")
                st.write(entry["name"])
                keyword_text = " · ".join(entry["keywords"])
                detail = keyword_text
                if entry["rarity"]:
                    detail += f" · {entry['rarity']}"
                st.caption(f"✦ {detail}")

    result_text = "\n".join(
        f"{index}. {entry['sinner']} — {entry['name']} "
        f"({', '.join(entry['keywords'])}"
        f"{', ' + entry['rarity'] if entry['rarity'] else ''})"
        for index, entry in enumerate(deck, start=1)
    )
    st.download_button(
        "📥 추첨 결과 다운로드 (.txt)",
        data=result_text,
        file_name="limbus_random_deck.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.text_area("결과 텍스트 (복사 가능)", value=result_text, height=150)
else:
    st.info("아직 추첨 결과가 없습니다. 왼쪽에서 키워드와 인원수를 선택한 뒤 '랜덤 덱 생성'을 눌러 주세요.")

with st.expander("등록된 인격 목록 확인"):
    for sinner in st.session_state.identity_data:
        with st.container(border=True):
            st.markdown(f"**{sinner['sinner']}**")
            for keyword in KEYWORDS:
                names = [
                    normalize_identity(item)
                    for item in sinner.get(keyword, [])
                ]
                names = [item for item in names if item]
                if names:
                    st.write(f"- **{keyword}:** " + ", ".join(
                        item["name"] + (f" ({item['rarity']})" if item["rarity"] else "")
                        for item in names
                    ))

st.caption(
    "※ 초기 인격 데이터는 편집 가능한 참고용 초안입니다. "
    "실제 게임 내 인격 이름과 키워드 분류는 사용 전에 확인해 주세요."
)

