import calendar

import streamlit as st


# ============================================================
# BASIC HELPERS
# ============================================================

def get_event_label(event):
    return f"{event.get('emoji', '')} {event.get('subject', '')}".strip()


def get_short_subject(subject):
    mapping = {
        "Tiếng Anh": "Anh",
        "Toán": "Toán",
        "Vật lý": "Lý",
    }
    return mapping.get(subject, subject)


def build_day_button_label(
    day_number,
    events,
    is_today=False,
    is_selected=False,
):
    """
    Tạo nội dung hiển thị trong ô ngày.

    Quy tắc:
    - Dòng đầu: số ngày.
    - Các dòng tiếp theo: emoji + tên môn ngắn.
    - Ngày đang chọn: thêm ✅ ở cuối ô.
    - Không hiển thị chữ "Đang chọn".
    - Không dùng dấu tích ở đầu ngày.
    """
    lines = [str(day_number)]

    for event in events:
        emoji = event.get("emoji", "")
        subject = get_short_subject(event.get("subject", ""))
        lines.append(f"{emoji} {subject}".strip())

    if is_today:
        lines.append("Hôm nay")

    if is_selected:
        lines.append("✅")

    return "\n".join(lines)


def get_event_color_key(event):
    emoji_map = {
        "🔴": "red",
        "🟠": "orange",
        "🟡": "yellow",
        "🟢": "green",
        "🔵": "blue",
        "⚫": "black",
        "🟣": "purple",
    }

    return emoji_map.get(
        event.get("emoji"),
        "neutral",
    )


def _safe_value(value):
    """
    Chuyển giá trị None, chuỗi rỗng thành dấu '-'.
    """
    if value is None:
        return "-"

    if isinstance(value, str) and not value.strip():
        return "-"

    return value


# ============================================================
# CSS
# ============================================================

def inject_dashboard_css():
    st.markdown(
        """
        <style>

        /* ==============================================
           DESIGN TOKENS
        ============================================== */

        :root {
            --bg-page: #f6f7fb;
            --bg-card: #ffffff;
            --bg-soft: #eef0f7;
            --bg-disabled: #e5e8f0;

            --text-main: #172033;
            --text-soft: #687086;
            --text-disabled: #8a91a3;

            --border: rgba(23, 32, 51, 0.10);
            --border-strong: rgba(23, 32, 51, 0.16);

            --accent: #6571d8;
            --accent-soft: rgba(101, 113, 216, 0.12);

            --shadow:
                0 12px 32px rgba(23, 32, 51, 0.07);

            --radius-lg: 22px;
            --radius-md: 16px;
            --radius-sm: 12px;
        }


        /* ==============================================
           PAGE
        ============================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at top left,
                    rgba(101, 113, 216, 0.11),
                    transparent 30rem
                ),
                var(--bg-page);

            color: var(--text-main);
        }


        .block-container {
            max-width: 1600px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }


        /* ==============================================
           APP HEADER
        ============================================== */

        .app-header {
            margin-bottom: 1rem;
        }


        .app-eyebrow {
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            color: var(--accent);
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }


        .app-header h1 {
            margin: 0;

            font-size:
                clamp(2rem, 4vw, 3.25rem);

            line-height: 1.05;
            letter-spacing: -0.04em;

            color: var(--text-main);
        }


        .app-header p {
            margin-top: 0.55rem;
            margin-bottom: 0;

            color: var(--text-soft);
            font-size: 1rem;
        }


        /* ==============================================
           GENERIC CARDS
        ============================================== */

        .content-card {
            width: 100%;
            box-sizing: border-box;

            background: var(--bg-card);

            border:
                1px solid var(--border);

            border-radius:
                var(--radius-lg);

            box-shadow:
                var(--shadow);

            padding:
                1rem 1.05rem;

            overflow-wrap: anywhere;
        }


        .section-label {
            font-size: 0.74rem;
            font-weight: 800;

            letter-spacing: 0.12em;

            text-transform: uppercase;

            color: var(--text-soft);

            margin-bottom: 0.45rem;
        }


        /* ==============================================
           TODAY HERO
        ============================================== */

        .today-card {
            width: 100%;
            box-sizing: border-box;

            background: #ffffff;

            border:
                1px solid var(--border);

            border-radius:
                var(--radius-lg);

            box-shadow:
                var(--shadow);

            padding:
                1rem 1.1rem;

            margin-bottom:
                1rem;
        }


        .hero-date {
            font-size:
                clamp(1.3rem, 2.4vw, 1.85rem);

            font-weight: 750;

            letter-spacing:
                -0.025em;

            color:
                var(--text-main);

            margin-top:
                0.25rem;
        }


        .hero-block {
            display: inline-flex;
            align-items: center;

            margin-top:
                0.55rem;

            padding:
                0.42rem 0.7rem;

            border-radius:
                999px;

            background:
                var(--accent-soft);

            color:
                var(--accent);

            font-size:
                0.88rem;

            font-weight:
                700;
        }


        .hero-list {
            margin:
                0.8rem 0 0;

            padding-left:
                1.15rem;

            color:
                var(--text-main);
        }


        .hero-list li {
            margin-bottom:
                0.45rem;
        }


        .hero-empty {
            margin-top:
                0.8rem;

            padding:
                0.75rem 0.85rem;

            border-radius:
                var(--radius-md);

            background:
                var(--bg-soft);

            color:
                var(--text-soft);
        }


        /* ==============================================
           QUICK STATS
        ============================================== */

        .stat-card {
            width: 100%;
            min-height: 100px;

            box-sizing: border-box;

            display: flex;
            flex-direction: column;
            justify-content: center;

            background:
                var(--bg-soft);

            border:
                1px solid var(--border);

            border-radius:
                var(--radius-md);

            padding:
                0.85rem 0.95rem;

            overflow-wrap:
                anywhere;
        }


        .stat-label {
            color:
                var(--text-soft);

            font-size:
                0.72rem;

            font-weight:
                800;

            letter-spacing:
                0.1em;

            text-transform:
                uppercase;
        }


        .stat-value {
            margin-top:
                0.42rem;

            font-size:
                1.2rem;

            font-weight:
                750;

            letter-spacing:
                -0.02em;

            color:
                var(--text-main);
        }


        /* ==============================================
           BUTTONS
        ============================================== */

        div[data-testid="stButton"] > button {
            width: 100%;

            min-height: 44px;

            box-sizing:
                border-box;

            border-radius:
                14px;

            border:
                1px solid var(--border-strong);

            background:
                #ffffff;

            color:
                var(--text-main);

            white-space:
                pre-wrap;

            overflow-wrap:
                anywhere;

            line-height:
                1.28;

            transition:
                transform 120ms ease,
                box-shadow 120ms ease,
                border-color 120ms ease,
                background 120ms ease;
        }


        div[data-testid="stButton"] > button:hover {
            background:
                #ffffff;

            border-color:
                rgba(101, 113, 216, 0.55);

            transform:
                translateY(-1px);

            box-shadow:
                0 6px 18px
                rgba(23, 32, 51, 0.08);
        }


        div[data-testid="stButton"] > button:active {
            transform:
                scale(0.985);
        }


        div[data-testid="stButton"] > button:disabled {
            background:
                var(--bg-disabled);

            color:
                var(--text-disabled);

            border-color:
                transparent;

            opacity:
                1;
        }


        /* ==============================================
           MONTH TOOLBAR
        ============================================== */

        .month-title {
            width: 100%;

            box-sizing: border-box;

            text-align: center;

            padding:
                0.25rem 0.5rem;
        }


        .month-title-value {
            font-size:
                1.08rem;

            font-weight:
                750;

            color:
                var(--text-main);
        }


        /* Selectbox interaction hierarchy */

        div[data-baseweb="select"] > div {
            background:
                #ffffff !important;

            color:
                var(--text-main) !important;

            border:
                1px solid var(--border-strong) !important;

            border-radius:
                12px !important;

            min-height:
                44px;
        }


        div[data-baseweb="select"] > div:hover {
            border-color:
                rgba(101, 113, 216, 0.55) !important;
        }


        /* ==============================================
           CALENDAR
        ============================================== */

        .calendar-section-title {
            margin-bottom:
                0.5rem;
        }


        .calendar-header {
            width: 100%;
            box-sizing: border-box;

            text-align: center;

            font-weight:
                700;

            padding:
                0.55rem 0.15rem;

            border-radius:
                0.7rem;

            background:
                var(--bg-soft);

            color:
                var(--text-main);

            margin-bottom:
                0.28rem;

            overflow-wrap:
                anywhere;
        }


        .day-empty {
            min-height:
                100px;

            border-radius:
                14px;

            border:
                1px dashed
                rgba(23, 32, 51, 0.08);

            background:
                rgba(238, 240, 247, 0.42);
        }


        /*
        Calendar buttons are identified through key-based
        Streamlit containers when supported by Streamlit.
        The general button styling remains the fallback.
        */

        div[data-testid="stButton"] > button p {
            margin:
                0;

            white-space:
                pre-wrap;

            overflow-wrap:
                anywhere;

            word-break:
                normal;
        }


        /* ==============================================
           DETAILS
        ============================================== */

        .details-header {
            width:
                100%;

            box-sizing:
                border-box;

            background:
                #ffffff;

            border:
                1px solid var(--border);

            border-radius:
                var(--radius-lg);

            box-shadow:
                var(--shadow);

            padding:
                1rem 1.05rem;

            margin-bottom:
                0.8rem;
        }


        .detail-card {
            width:
                100%;

            box-sizing:
                border-box;

            background:
                #ffffff;

            border:
                1px solid var(--border);

            border-radius:
                var(--radius-md);

            padding:
                0.9rem 1rem;

            margin-bottom:
                0.8rem;

            overflow-wrap:
                anywhere;
        }


        .detail-title {
            font-size:
                1.03rem;

            font-weight:
                750;

            margin-bottom:
                0.2rem;

            color:
                var(--text-main);
        }


        .detail-meta {
            color:
                var(--text-soft);

            font-size:
                0.9rem;

            margin-bottom:
                0.65rem;
        }


        .detail-pill-row {
            display:
                flex;

            flex-wrap:
                wrap;

            gap:
                0.4rem;

            margin:
                0.25rem 0 0.7rem;
        }


        .detail-pill {
            display:
                inline-flex;

            align-items:
                center;

            width:
                fit-content;

            max-width:
                100%;

            min-height:
                32px;

            padding:
                0.35rem 0.7rem;

            border-radius:
                999px;

            font-size:
                0.78rem;

            font-weight:
                700;

            background:
                var(--bg-soft);

            color:
                #2f3853;

            box-sizing:
                border-box;

            white-space:
                normal;

            overflow-wrap:
                anywhere;
        }


        .detail-content {
            color:
                var(--text-main);

            line-height:
                1.6;
        }


        .detail-content ul {
            margin-top:
                0.35rem;

            margin-bottom:
                0.8rem;
        }


        .detail-content li {
            margin-bottom:
                0.35rem;
        }


        .empty-detail {
            width:
                100%;

            box-sizing:
                border-box;

            padding:
                0.85rem;

            border-radius:
                var(--radius-md);

            background:
                var(--bg-soft);

            color:
                var(--text-soft);
        }


        /* ==============================================
           TABLET / IPAD
        ============================================== */

        @media (max-width: 1100px) {

            .block-container {
                padding-left:
                    0.8rem;

                padding-right:
                    0.8rem;
            }


            .stat-card {
                min-height:
                    96px;
            }


            div[data-testid="stButton"] > button {
                padding:
                    0.5rem 0.48rem;

                font-size:
                    0.92rem;
            }


            .calendar-header {
                font-size:
                    0.9rem;

                padding:
                    0.5rem 0.08rem;
            }

        }


        /* ==============================================
           SMALL TABLET
        ============================================== */

        @media (max-width: 820px) {

            .block-container {
                padding-left:
                    0.45rem;

                padding-right:
                    0.45rem;
            }


            .app-header h1 {
                font-size:
                    2rem;
            }


            .app-header p {
                font-size:
                    0.94rem;
            }


            .calendar-header {
                font-size:
                    0.82rem;
            }


            div[data-testid="stButton"] > button {
                padding:
                    0.48rem 0.35rem;

                font-size:
                    0.86rem;
            }


            .day-empty {
                min-height:
                    88px;
            }

        }


        /* ==============================================
           MOBILE
        ============================================== */

        @media (max-width: 600px) {

            .app-header p {
                font-size:
                    0.9rem;
            }


            .today-card,
            .details-header,
            .detail-card {
                padding:
                    0.8rem;
            }


            .stat-card {
                min-height:
                    88px;

                padding:
                    0.7rem;
            }


            .stat-value {
                font-size:
                    1.05rem;
            }


            .calendar-header {
                font-size:
                    0.72rem;

                padding:
                    0.45rem 0.03rem;
            }


            div[data-testid="stButton"] > button {
                padding:
                    0.42rem 0.22rem;

                font-size:
                    0.78rem;
            }


            .day-empty {
                min-height:
                    78px;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# APP HEADER
# ============================================================

def render_app_header():
    st.markdown(
        """
        <div class="app-header">
            <div class="app-eyebrow">
                STUDY CALENDAR
            </div>

            <h1>
                Lịch học của L
            </h1>

            <p>
                Học đúng nhịp · Nhớ lâu hơn ·
                Chỉ sửa đúng phần còn yếu
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# TODAY HERO
# ============================================================

def render_today_hero(
    today,
    events,
    start_date,
    block_number,
    format_vietnamese_date,
):
    html_parts = [
        '<div class="today-card">',
        '<div class="section-label">Hôm nay</div>',
        (
            '<div class="hero-date">'
            f'{format_vietnamese_date(today)}'
            '</div>'
        ),
    ]

    if block_number is not None:
        html_parts.append(
            (
                '<div class="hero-block">'
                f'Block {block_number}'
                '</div>'
            )
        )

    if today < start_date:
        html_parts.append(
            (
                '<div class="hero-empty">'
                'Chương trình bắt đầu từ '
                f'{start_date.strftime("%d/%m/%Y")}.'
                '</div>'
            )
        )

    elif not events:
        html_parts.append(
            (
                '<div class="hero-empty">'
                'Hôm nay không có nhiệm vụ học tập.'
                '</div>'
            )
        )

    else:
        html_parts.append(
            '<ul class="hero-list">'
        )

        for event in events:
            emoji = event.get("emoji", "")
            full_subject = event.get(
                "full_subject",
                event.get("subject", ""),
            )
            stage = event.get("stage", "")
            milestone = event.get("milestone", "")

            html_parts.append(
                (
                    '<li>'
                    f'<strong>{emoji} {full_subject}</strong>'
                    f' · {stage}'
                    f' · {milestone}'
                    '</li>'
                )
            )

        html_parts.append("</ul>")

    html_parts.append("</div>")

    st.markdown(
        "".join(html_parts),
        unsafe_allow_html=True,
    )


# ============================================================
# QUICK STATS
# ============================================================

def render_quick_stats(
    block_number,
    today_events_count,
    selected_date,
):
    """
    Chỉ có 3 ô thống kê.
    Ô 'Mốc tiếp theo' đã được loại bỏ hoàn toàn.
    """

    cols = st.columns(3)

    stat_data = [
        (
            "Block hiện tại",
            str(block_number or "—"),
        ),
        (
            "Nhiệm vụ hôm nay",
            f"{today_events_count} nhiệm vụ",
        ),
        (
            "Ngày đã chọn",
            selected_date.strftime("%d/%m/%Y"),
        ),
    ]

    for column, (label, value) in zip(
        cols,
        stat_data,
    ):
        with column:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        {label}
                    </div>

                    <div class="stat-value">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# MONTH TOOLBAR
# ============================================================

def render_month_toolbar(
    previous_month,
    next_month,
    go_to_today,
    go_to_purple_week,
):
    top = st.columns(
        [1, 2, 1],
        vertical_alignment="center",
    )

    with top[0]:
        st.button(
            "◀",
            on_click=previous_month,
            use_container_width=True,
            key="prev_month",
        )

    with top[1]:
        st.markdown(
            f"""
            <div class="month-title">
                <div class="section-label">
                    Tháng đang xem
                </div>

                <div class="month-title-value">
                    Tháng {st.session_state.view_month}
                    ·
                    {st.session_state.view_year}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with top[2]:
        st.button(
            "▶",
            on_click=next_month,
            use_container_width=True,
            key="next_month",
        )

    toolbar_cols = st.columns(
        [1, 1.25, 1, 1.25],
        vertical_alignment="bottom",
    )

    with toolbar_cols[0]:
        st.button(
            "Hôm nay",
            on_click=go_to_today,
            use_container_width=True,
            key="go_today",
        )

    with toolbar_cols[1]:
        st.button(
            "Tuần tím đầu tiên",
            on_click=go_to_purple_week,
            use_container_width=True,
            key="go_purple",
        )

    with toolbar_cols[2]:
        selected_month = st.selectbox(
            "Tháng",
            options=list(range(1, 13)),
            index=st.session_state.view_month - 1,
            format_func=lambda value: f"Tháng {value}",
            key="month_selector",
        )

    with toolbar_cols[3]:
        current_view_year = (
            st.session_state.view_year
        )

        year_options = list(
            range(
                current_view_year - 5,
                current_view_year + 21,
            )
        )

        selected_year = st.selectbox(
            "Năm",
            options=year_options,
            index=year_options.index(
                current_view_year
            ),
            key="year_selector",
        )

    if (
        selected_month
        != st.session_state.view_month
        or selected_year
        != st.session_state.view_year
    ):
        st.session_state.view_month = (
            selected_month
        )

        st.session_state.view_year = (
            selected_year
        )

        st.rerun()


# ============================================================
# CALENDAR GRID
# ============================================================

def render_calendar_grid(
    year,
    month,
    schedule,
    today,
    selected_date,
    select_date,
):
    st.markdown(
        '<div class="section-label calendar-section-title">'
        'Lịch tháng'
        '</div>',
        unsafe_allow_html=True,
    )

    headers = [
        "Thứ 2",
        "Thứ 3",
        "Thứ 4",
        "Thứ 5",
        "Thứ 6",
        "Thứ 7",
        "Chủ nhật",
    ]

    header_columns = st.columns(7)

    for index, header in enumerate(headers):
        with header_columns[index]:
            st.markdown(
                (
                    '<div class="calendar-header">'
                    f'{header}'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

    cal = calendar.Calendar(firstweekday=0)

    weeks = cal.monthdatescalendar(
        year,
        month,
    )

    for week in weeks:
        columns = st.columns(7)

        for index, current_date in enumerate(week):
            with columns[index]:

                if current_date.month != month:
                    st.markdown(
                        '<div class="day-empty"></div>',
                        unsafe_allow_html=True,
                    )
                    continue

                events = schedule.get(
                    current_date,
                    [],
                )

                is_today = (
                    current_date == today
                )

                is_selected = (
                    current_date == selected_date
                )

                visible_events = events[:2]

                button_label = build_day_button_label(
                    current_date.day,
                    visible_events,
                    is_today=is_today,
                    is_selected=is_selected,
                )

                if len(events) > 2:
                    extra_count = len(events) - 2

                    if is_selected:
                        lines = button_label.split("\n")

                        if lines and lines[-1] == "✅":
                            lines.insert(
                                -1,
                                f"+{extra_count} khác",
                            )
                        else:
                            lines.append(
                                f"+{extra_count} khác"
                            )

                        button_label = "\n".join(lines)

                    else:
                        button_label = (
                            f"{button_label}\n"
                            f"+{extra_count} khác"
                        )

                button_type = (
                    "primary"
                    if is_selected
                    else "secondary"
                )

                st.button(
                    button_label,
                    key=(
                        f"day_"
                        f"{current_date.isoformat()}"
                    ),
                    on_click=select_date,
                    args=(current_date,),
                    use_container_width=True,
                    type=button_type,
                )


# ============================================================
# SELECTED DAY DETAILS
# ============================================================

def render_selected_day_details(
    selected_date,
    selected_events,
    block_number,
    format_vietnamese_date,
    get_day_type_details,
    error_types,
    repair_statuses,
):
    header_parts = [
        '<div class="details-header">',
        (
            '<div class="section-label">'
            'Chi tiết ngày đã chọn'
            '</div>'
        ),
        (
            '<div class="hero-date">'
            f'{format_vietnamese_date(selected_date)}'
            '</div>'
        ),
    ]

    if block_number is not None:
        header_parts.append(
            (
                '<div class="hero-block">'
                f'Block {block_number}'
                f' · {len(selected_events)} nhiệm vụ'
                '</div>'
            )
        )

    header_parts.append("</div>")

    st.markdown(
        "".join(header_parts),
        unsafe_allow_html=True,
    )

    if not selected_events:
        st.markdown(
            """
            <div class="empty-detail">
                Không có nhiệm vụ học tập
                trong ngày này.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for event in selected_events:
        emoji = event.get("emoji", "")

        full_subject = event.get(
            "full_subject",
            event.get("subject", ""),
        )

        stage = event.get(
            "stage",
            "-",
        )

        milestone = event.get(
            "milestone",
            "-",
        )

        detail_map = {
            "study_mode": _safe_value(
                event.get("study_mode")
            ),
            "start_time": _safe_value(
                event.get("start_time")
            ),
            "duration": _safe_value(
                event.get("duration")
            ),
        }

        if detail_map["study_mode"] == "-":
            fallback_details = (
                get_day_type_details(stage)
            )

            detail_map = {
                "study_mode": _safe_value(
                    fallback_details.get(
                        "study_mode"
                    )
                ),
                "start_time": _safe_value(
                    fallback_details.get(
                        "start_time"
                    )
                ),
                "duration": _safe_value(
                    fallback_details.get(
                        "duration"
                    )
                ),
            }

        card_parts = [
            '<div class="detail-card">',
            (
                '<div class="detail-title">'
                f'{emoji} {full_subject}'
                f' · {stage}'
                '</div>'
            ),
            (
                '<div class="detail-meta">'
                f'Mốc: {milestone}'
                '</div>'
            ),
            '<div class="detail-pill-row">',
            (
                '<div class="detail-pill">'
                'Hình thức học: '
                f'{detail_map["study_mode"]}'
                '</div>'
            ),
            (
                '<div class="detail-pill">'
                'Giờ bắt đầu: '
                f'{detail_map["start_time"]}'
                '</div>'
            ),
            (
                '<div class="detail-pill">'
                'Thời lượng: '
                f'{detail_map["duration"]}'
                '</div>'
            ),
            '</div>',
        ]

        tasks = event.get("tasks", [])

        if tasks:
            card_parts.append(
                '<div class="detail-content">'
            )

            card_parts.append(
                '<strong>Cần làm:</strong>'
            )

            card_parts.append("<ul>")

            for task in tasks:
                card_parts.append(
                    f"<li>{task}</li>"
                )

            card_parts.append("</ul>")

            card_parts.append("</div>")

        check_method = _safe_value(
            event.get("check_method")
        )

        goal = _safe_value(
            event.get("goal")
        )

        card_parts.append(
            (
                '<div class="detail-content">'
                '<p>'
                '<strong>Hình thức kiểm tra:</strong> '
                f'{check_method}'
                '</p>'
                '<p>'
                '<strong>Mục tiêu:</strong> '
                f'{goal}'
                '</p>'
                '</div>'
            )
        )

        notes = event.get("notes", [])

        if notes:
            card_parts.append(
                '<div class="detail-content">'
            )

            card_parts.append(
                '<strong>Lưu ý:</strong>'
            )

            card_parts.append("<ul>")

            for note in notes:
                card_parts.append(
                    f"<li>{note}</li>"
                )

            card_parts.append("</ul>")

            card_parts.append("</div>")

        card_parts.append("</div>")

        st.markdown(
            "".join(card_parts),
            unsafe_allow_html=True,
        )

        if event.get("type") == "test":
            with st.expander(
                "Xem cách phân loại lỗi sau kiểm tra"
            ):
                for error in error_types:
                    st.markdown(
                        (
                            f"**{error['code']}. "
                            f"{error['name']}**"
                        )
                    )

                    st.markdown(
                        (
                            "- Biểu hiện: "
                            f"{error['symptom']}"
                        )
                    )

                    st.markdown(
                        (
                            "- Xử lý: "
                            f"{error['action']}"
                        )
                    )

        if event.get("type") == "repair":
            priority_order = event.get(
                "priority_order",
                [],
            )

            if priority_order:
                st.markdown(
                    "**Thứ tự ưu tiên xử lý:**"
                )

                for number, item in enumerate(
                    priority_order,
                    start=1,
                ):
                    st.markdown(
                        f"{number}. {item}"
                    )

            st.markdown(
                "**Trạng thái sau khi xử lý:**"
            )

            for status in repair_statuses:
                st.markdown(
                    (
                        f"{status['emoji']} "
                        f"**{status['name']}** — "
                        f"{status['meaning']} "
                        f"**Xử lý tiếp:** "
                        f"{status['next_action']}"
                    )
                )


# ============================================================
# LEARNING RULE SECTIONS
# ============================================================

def render_learning_rule_sections(
    prerequisite_rules,
    persistent_gap_rule,
    purple_review_info,
):
    st.divider()

    with st.expander(
        "🧠 Quy tắc xử lý kiến thức tiên quyết"
    ):
        st.markdown(
            (
                "**Không liên quan trực tiếp đến "
                "block tiếp theo:** "
                f"{prerequisite_rules[
                    'not_required_for_next_block'
                ]}"
            )
        )

        st.markdown(
            (
                "**Là điều kiện tiên quyết bắt buộc:** "
                f"{prerequisite_rules[
                    'required_for_next_block'
                ]}"
            )
        )

        st.markdown(
            (
                "**Lỗ hổng nghiêm trọng:** "
                f"{prerequisite_rules[
                    'severe_gap'
                ]}"
            )
        )

    with st.expander(
        "🔁 Quy tắc lỗ hổng dai dẳng"
    ):
        st.markdown(
            persistent_gap_rule
        )

    with st.expander(
        "📖 Chú thích các màu"
    ):
        st.markdown(
            """
            🔴 **Ngày đỏ — Ngày 0:** Kiểm tra bài cũ
            hoặc nợ kiến thức và dạy kiến thức mới.

            🟠 **Ngày cam — Ngày 1:** Tự nhớ, chép lại
            và kiểm tra kết quả qua ảnh.

            🟡 **Ngày vàng — Ngày 3:** Đọc lại, làm bài tập,
            tự giải thích và kiểm tra kết quả qua video.

            🟢 **Ngày xanh lá — Ngày 7:** Củng cố,
            làm bài và chữa trực tiếp online.

            🔵 **Ngày xanh dương:** Bài kiểm tra chẩn đoán
            cuối block.

            ⚫ **Ngày đen:** Vá đúng những đơn vị kiến thức
            cần xử lý.

            🟣 **Ngày tím:** Tổng ôn định kỳ sau mỗi 4 block.
            """
        )

    with st.expander(
        "🟣 Quy tắc ngày tím"
    ):
        st.markdown(
            (
                "**Mốc:** "
                f"{purple_review_info.get(
                    'milestone',
                    '-'
                )}"
            )
        )

        tasks = purple_review_info.get(
            "tasks",
            [],
        )

        if tasks:
            st.markdown(
                "**Cần làm:**"
            )

            for task in tasks:
                st.markdown(
                    f"- {task}"
                )

        priority = purple_review_info.get(
            "priority",
            [],
        )

        if priority:
            st.markdown(
                "**Ưu tiên:**"
            )

            for item in priority:
                st.markdown(
                    f"- {item}"
                )

        st.markdown(
            (
                "**Lưu ý:** "
                f"{purple_review_info.get(
                    'note',
                    '-'
                )}"
            )
        )