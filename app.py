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
        st.session_state.custom_keywords = []
        st.rerun()

candidates = build_candidates(
    st.session_state.identity_data,
    selected_keyword,
    all_keywords,
)
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
            for keyword in all_keywords:
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
    "※ 추가 키워드와 인격 등록 내용은 현재 브라우저 세션 동안 유지됩니다. "
    "앱을 새로 시작하면 초기화될 수 있습니다. "
    "초기 인격 데이터는 편집 가능한 참고용 초안이므로 실제 게임 내 분류를 확인해 주세요."
)
