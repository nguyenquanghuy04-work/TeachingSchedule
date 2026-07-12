import calendar
import html

import streamlit as st


# ============================================================
# BASIC HELPERS
# ============================================================

def escape_text(value):
    """Escape dynamic text before inserting it into HTML."""
    return html.escape(str(value))


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
    lines = [str(day_number)]

    for event in events:
        emoji = event.get("emoji", "")
        subject = get_short_subject(
            event.get("full_subject")
            or event.get("subject", "")
        )
        lines.append(f"{emoji} {subject}".strip())

    if is_today:
        lines.append("• Hôm nay")

    if is_selected:
        lines[-1] = f"{lines[-1]}  ✅"

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
    return emoji_map.get(event.get("emoji"), "neutral")


def _safe_event_subject(event):
    return (
        event.get("full_subject")
        or event.get("subject")
        or "Môn học"
    )


def _render_html(content):
    """
    Render one complete HTML fragment in one Streamlit markdown call.
    This avoids Streamlit displaying HTML tags as literal text.
    """
    st.markdown(
        content.strip(),
        unsafe_allow_html=True,
    )


# ============================================================
# CSS
# ============================================================

def inject_dashboard_css():
    st.markdown(
        """
<style>
:root {
    --bg-page: #f6f7fb;
    --bg-card: rgba(255, 255, 255, 0.96);
    --bg-muted: #eef0f7;

    --text-main: #172033;
    --text-soft: #687086;

    --border: rgba(23, 32, 51, 0.09);
    --border-strong: rgba(23, 32, 51, 0.14);

    --accent: #6571d8;
    --accent-soft: rgba(101, 113, 216, 0.10);

    --shadow:
        0 14px 40px rgba(23, 32, 51, 0.07);

    --radius-lg: 22px;
    --radius-md: 16px;
    --radius-sm: 12px;
}


/* =========================================================
   PAGE
   ========================================================= */

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


/* =========================================================
   HEADER
   ========================================================= */

.app-header {
    margin-bottom: 1rem;
}

.app-eyebrow {
    margin-bottom: 0.35rem;

    color: var(--accent);

    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

.app-header h1 {
    margin: 0;

    color: var(--text-main);

    font-size: clamp(2rem, 4vw, 3.25rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.04em;
}

.app-header p {
    margin: 0.55rem 0 0;

    color: var(--text-soft);

    font-size: 1rem;
    line-height: 1.55;
}


/* =========================================================
   GENERAL CARDS
   ========================================================= */

.glass-card {
    width: 100%;
    box-sizing: border-box;

    padding: 1rem;

    background: var(--bg-card);

    border: 1px solid var(--border);
    border-radius: var(--radius-lg);

    box-shadow: var(--shadow);

    overflow-wrap: anywhere;
}

.section-label {
    margin-bottom: 0.45rem;

    color: var(--text-soft);

    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    line-height: 1.35;
    text-transform: uppercase;
}


/* =========================================================
   TODAY HERO
   ========================================================= */

.today-card {
    margin-bottom: 1rem;
}

.hero-date {
    margin-top: 0.25rem;

    color: var(--text-main);

    font-size: clamp(1.25rem, 2.4vw, 1.85rem);
    font-weight: 800;
    line-height: 1.25;
    letter-spacing: -0.025em;

    overflow-wrap: anywhere;
}

.hero-block {
    display: inline-flex;
    align-items: center;

    width: fit-content;
    max-width: 100%;

    margin-top: 0.65rem;
    padding: 0.42rem 0.72rem;

    background: var(--accent-soft);
    color: var(--accent);

    border-radius: 999px;

    font-size: 0.88rem;
    font-weight: 750;

    box-sizing: border-box;
    white-space: normal;
    overflow-wrap: anywhere;
}

.hero-list {
    margin: 0.85rem 0 0;
    padding-left: 1.35rem;

    color: var(--text-main);
}

.hero-list li {
    margin-bottom: 0.5rem;
    line-height: 1.55;
}


/* =========================================================
   QUICK STATS
   ========================================================= */

.stat-card {
    width: 100%;
    min-height: 100px;
    box-sizing: border-box;

    padding: 0.9rem 1rem;

    background: var(--bg-muted);

    border: 1px solid rgba(23, 32, 51, 0.06);
    border-radius: var(--radius-md);

    overflow: hidden;
    overflow-wrap: anywhere;
}

.stat-label {
    color: var(--text-soft);

    font-size: 0.72rem;
    font-weight: 800;
    line-height: 1.35;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.stat-value {
    margin-top: 0.45rem;

    color: var(--text-main);

    font-size: clamp(1rem, 2vw, 1.2rem);
    font-weight: 800;
    line-height: 1.35;
    letter-spacing: -0.02em;

    overflow-wrap: anywhere;
}


/* =========================================================
   MONTH TITLE
   ========================================================= */

.month-title-wrapper {
    width: 100%;

    padding: 0.25rem 0.4rem;

    text-align: center;
    box-sizing: border-box;
}

.month-title-label {
    margin-bottom: 0.35rem;

    color: var(--text-soft);

    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.month-title-value {
    color: var(--text-main);

    font-size: 1.1rem;
    font-weight: 800;
    line-height: 1.35;

    overflow-wrap: anywhere;
}


/* =========================================================
   STREAMLIT BUTTONS
   ========================================================= */

div[data-testid="stButton"] > button {
    width: 100%;

    min-height: 46px;

    padding: 0.55rem 0.65rem;

    background: #ffffff;
    color: var(--text-main);

    border: 1px solid var(--border-strong);
    border-radius: 14px;

    box-sizing: border-box;

    text-align: center;

    white-space: pre-wrap;
    overflow-wrap: anywhere;
    word-break: normal;

    line-height: 1.3;

    transition:
        transform 120ms ease,
        box-shadow 120ms ease,
        border-color 120ms ease;
}

div[data-testid="stButton"] > button:hover {
    border-color: rgba(101, 113, 216, 0.5);

    transform: translateY(-1px);

    box-shadow:
        0 6px 18px rgba(23, 32, 51, 0.08);
}

div[data-testid="stButton"] > button:active {
    transform: scale(0.985);
}

div[data-testid="stButton"] > button:disabled {
    background: #e9ecf3;
    color: #7b8498;

    border-color: rgba(23, 32, 51, 0.07);

    opacity: 1;
}


/* =========================================================
   SELECTBOX
   ========================================================= */

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: var(--text-main) !important;

    border: 1px solid var(--border-strong) !important;
    border-radius: 14px !important;

    min-height: 46px;
}


/* =========================================================
   CALENDAR
   ========================================================= */

.calendar-header {
    width: 100%;
    box-sizing: border-box;

    padding: 0.55rem 0.15rem;
    margin-bottom: 0.3rem;

    background: rgba(128, 128, 128, 0.11);
    color: var(--text-main);

    border-radius: 0.7rem;

    text-align: center;

    font-size: 0.9rem;
    font-weight: 750;
    line-height: 1.25;

    overflow-wrap: anywhere;
}

.calendar-placeholder {
    min-height: 108px;

    background: #f0f2f7;

    border:
        1px dashed rgba(23, 32, 51, 0.09);

    border-radius: 14px;

    box-sizing: border-box;
}


/* Calendar day buttons */
.calendar-grid-marker
+ div
div[data-testid="stButton"] > button {
    min-height: 108px;

    align-items: flex-start;
    justify-content: flex-start;

    padding: 0.55rem 0.5rem;

    background: #ffffff;

    text-align: left;

    font-size: 0.86rem;
    line-height: 1.3;
}


/* =========================================================
   DETAIL CARD
   ========================================================= */

.detail-card {
    width: 100%;
    box-sizing: border-box;

    margin-top: 0.85rem;
    padding: 0.95rem;

    background: #ffffff;

    border: 1px solid var(--border);
    border-radius: 16px;

    overflow-wrap: anywhere;
}

.detail-title {
    margin-bottom: 0.25rem;

    color: var(--text-main);

    font-size: 1.03rem;
    font-weight: 800;
    line-height: 1.4;

    overflow-wrap: anywhere;
}

.detail-meta {
    margin-bottom: 0.7rem;

    color: var(--text-soft);

    font-size: 0.9rem;
    line-height: 1.4;
}

.detail-pill {
    display: inline-flex;
    align-items: center;

    width: fit-content;
    max-width: 100%;
    min-height: 32px;

    margin-right: 0.35rem;
    margin-bottom: 0.4rem;

    padding: 0.35rem 0.7rem;

    background: #eef0f7;
    color: #2f3853;

    border-radius: 999px;

    box-sizing: border-box;

    font-size: 0.78rem;
    font-weight: 700;
    line-height: 1.35;

    white-space: normal;
    overflow-wrap: anywhere;
}


/* =========================================================
   RESPONSIVE — IPAD / TABLET
   ========================================================= */

@media (max-width: 1100px) {

    .block-container {
        padding-left: 0.65rem;
        padding-right: 0.65rem;
    }

    .glass-card {
        padding: 0.9rem;
    }

    .stat-card {
        min-height: 96px;
        padding: 0.8rem;
    }

    .calendar-header {
        font-size: 0.84rem;
    }

    .calendar-grid-marker
    + div
    div[data-testid="stButton"] > button {
        min-height: 100px;
        padding: 0.48rem 0.42rem;
        font-size: 0.8rem;
    }
}


/* =========================================================
   RESPONSIVE — SMALL TABLET
   ========================================================= */

@media (max-width: 820px) {

    .block-container {
        padding-left: 0.45rem;
        padding-right: 0.45rem;
    }

    .app-header h1 {
        font-size: 2rem;
    }

    .app-header p {
        font-size: 0.94rem;
    }

    .glass-card {
        border-radius: 18px;
    }

    .calendar-header {
        padding-left: 0.05rem;
        padding-right: 0.05rem;

        font-size: 0.76rem;
    }

    .calendar-grid-marker
    + div
    div[data-testid="stButton"] > button {
        min-height: 92px;

        padding: 0.4rem 0.32rem;

        font-size: 0.75rem;
        line-height: 1.25;
    }
}


/* =========================================================
   RESPONSIVE — MOBILE
   ========================================================= */

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.3rem;
        padding-right: 0.3rem;
    }

    .app-header h1 {
        font-size: 1.8rem;
    }

    .app-header p {
        font-size: 0.9rem;
    }

    .calendar-header {
        font-size: 0.67rem;
    }

    .calendar-grid-marker
    + div
    div[data-testid="stButton"] > button {
        min-height: 84px;

        padding: 0.35rem 0.25rem;

        font-size: 0.68rem;
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
    _render_html(
        """
        <div class="app-header">
            <div class="app-eyebrow">STUDY CALENDAR</div>
            <h1>Lịch học của L</h1>
            <p>
                Học đúng nhịp · Nhớ lâu hơn ·
                Chỉ sửa đúng phần còn yếu
            </p>
        </div>
        """
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
    content_parts = [
        '<div class="glass-card today-card">',
        '<div class="section-label">Hôm nay</div>',
        (
            '<div class="hero-date">'
            f'{escape_text(format_vietnamese_date(today))}'
            '</div>'
        ),
    ]

    if block_number is not None:
        content_parts.append(
            '<div class="hero-block">'
            f'Block {escape_text(block_number)}'
            '</div>'
        )

    if today < start_date:
        content_parts.append(
            '<p class="detail-meta" style="margin-top:0.8rem;">'
            'Chương trình bắt đầu từ '
            f'{escape_text(start_date.strftime("%d/%m/%Y"))}.'
            '</p>'
        )

    elif not events:
        content_parts.append(
            '<p class="detail-meta" style="margin-top:0.8rem;">'
            'Hôm nay không có nhiệm vụ học tập.'
            '</p>'
        )

    else:
        content_parts.append('<ul class="hero-list">')

        for event in events:
            emoji = escape_text(event.get("emoji", ""))
            subject = escape_text(_safe_event_subject(event))
            stage = escape_text(event.get("stage", "-"))
            milestone = escape_text(event.get("milestone", "-"))

            content_parts.append(
                "<li>"
                f"<strong>{emoji} {subject}</strong>"
                f" · {stage} · {milestone}"
                "</li>"
            )

        content_parts.append("</ul>")

    content_parts.append("</div>")

    _render_html("".join(content_parts))


# ============================================================
# QUICK STATS
# ============================================================

def render_quick_stats(
    block_number,
    today_events_count,
    selected_date,
):
    stats = [
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

    cols = st.columns(3)

    for column, (label, value) in zip(cols, stats):
        with column:
            _render_html(
                '<div class="stat-card">'
                f'<div class="stat-label">{escape_text(label)}</div>'
                f'<div class="stat-value">{escape_text(value)}</div>'
                '</div>'
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
    top = st.columns([1, 2.2, 1])

    with top[0]:
        st.button(
            "◀",
            on_click=previous_month,
            use_container_width=True,
            key="prev_month",
        )

    with top[1]:
        _render_html(
            '<div class="month-title-wrapper">'
            '<div class="month-title-label">'
            'Tháng đang xem'
            '</div>'
            '<div class="month-title-value">'
            f'Tháng {escape_text(st.session_state.view_month)}'
            ' · '
            f'{escape_text(st.session_state.view_year)}'
            '</div>'
            '</div>'
        )

    with top[2]:
        st.button(
            "▶",
            on_click=next_month,
            use_container_width=True,
            key="next_month",
        )

    toolbar_cols = st.columns([1, 1.3, 1, 1])

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
        current_view_year = st.session_state.view_year

        start_year = min(
            2020,
            current_view_year - 5,
        )

        end_year = max(
            2050,
            current_view_year + 20,
        )

        year_options = list(
            range(start_year, end_year + 1)
        )

        selected_year = st.selectbox(
            "Năm",
            options=year_options,
            index=year_options.index(current_view_year),
            key="year_selector",
        )

    if (
        selected_month != st.session_state.view_month
        or selected_year != st.session_state.view_year
    ):
        st.session_state.view_month = selected_month
        st.session_state.view_year = selected_year
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
    _render_html(
        '<div class="section-label">Lịch tháng</div>'
    )

    header_columns = st.columns(7)

    headers = [
        "Thứ 2",
        "Thứ 3",
        "Thứ 4",
        "Thứ 5",
        "Thứ 6",
        "Thứ 7",
        "Chủ nhật",
    ]

    for index, header in enumerate(headers):
        with header_columns[index]:
            _render_html(
                '<div class="calendar-header">'
                f'{escape_text(header)}'
                '</div>'
            )

    # Marker used by CSS to scope calendar button styling.
    _render_html(
        '<div class="calendar-grid-marker"></div>'
    )

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(year, month)

    for week in weeks:
        columns = st.columns(7)

        for index, current_date in enumerate(week):
            with columns[index]:

                if current_date.month != month:
                    _render_html(
                        '<div class="calendar-placeholder"></div>'
                    )
                    continue

                events = schedule.get(current_date, [])

                is_today = current_date == today
                is_selected = current_date == selected_date

                visible_events = events[:2]

                button_label = build_day_button_label(
                    current_date.day,
                    visible_events,
                    is_today=is_today,
                    is_selected=is_selected,
                )

                if len(events) > 2:
                    button_label += (
                        f"\n+{len(events) - 2} khác"
                    )

                st.button(
                    button_label,
                    key=f"day_{current_date.isoformat()}",
                    on_click=select_date,
                    args=(current_date,),
                    use_container_width=True,
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
    _render_html(
        '<div class="section-label">'
        'Chi tiết ngày đã chọn'
        '</div>'
        '<div class="hero-date">'
        f'{escape_text(format_vietnamese_date(selected_date))}'
        '</div>'
    )

    if block_number is not None:
        _render_html(
            '<div class="hero-block">'
            f'Block {escape_text(block_number)}'
            ' · '
            f'{escape_text(len(selected_events))} nhiệm vụ'
            '</div>'
        )

    if not selected_events:
        st.info(
            "Không có nhiệm vụ học tập trong ngày này."
        )
        return

    for event in selected_events:
        subject = _safe_event_subject(event)

        stage = event.get("stage", "-")
        milestone = event.get("milestone", "-")
        emoji = event.get("emoji", "")

        _render_html(
            '<div class="detail-card">'
            '<div class="detail-title">'
            f'{escape_text(emoji)} '
            f'{escape_text(subject)}'
            ' · '
            f'{escape_text(stage)}'
            '</div>'
            '<div class="detail-meta">'
            'Mốc: '
            f'{escape_text(milestone)}'
            '</div>'
            '</div>'
        )

        detail_map = {
            "study_mode": event.get("study_mode", "-"),
            "start_time": event.get("start_time", "-"),
            "duration": event.get("duration", "-"),
        }

        if (
            not detail_map["study_mode"]
            or detail_map["study_mode"] == "-"
        ):
            fallback_details = get_day_type_details(stage)

            if fallback_details:
                detail_map = {
                    "study_mode": fallback_details.get(
                        "study_mode",
                        "-",
                    ),
                    "start_time": fallback_details.get(
                        "start_time",
                        "-",
                    ),
                    "duration": fallback_details.get(
                        "duration",
                        "-",
                    ),
                }

        pills_html = "".join(
            [
                '<div class="detail-pill">'
                'Hình thức học: '
                f'{escape_text(detail_map["study_mode"])}'
                '</div>',

                '<div class="detail-pill">'
                'Giờ bắt đầu: '
                f'{escape_text(detail_map["start_time"])}'
                '</div>',

                '<div class="detail-pill">'
                'Thời lượng: '
                f'{escape_text(detail_map["duration"])}'
                '</div>',
            ]
        )

        _render_html(pills_html)

        if event.get("tasks"):
            st.markdown("**Cần làm:**")

            for task in event["tasks"]:
                st.markdown(f"- {task}")

        st.markdown(
            "**Hình thức kiểm tra:** "
            f"{event.get('check_method', '-')}"
        )

        st.markdown(
            "**Mục tiêu:** "
            f"{event.get('goal', '-')}"
        )

        if event.get("notes"):
            st.markdown("**Lưu ý:**")

            for note in event["notes"]:
                st.markdown(f"- {note}")

        if event.get("type") == "test":
            with st.expander(
                "Xem cách phân loại lỗi sau kiểm tra"
            ):
                for error in error_types:
                    st.markdown(
                        f"**{error['code']}. "
                        f"{error['name']}**"
                    )

                    st.markdown(
                        f"- Biểu hiện: "
                        f"{error['symptom']}"
                    )

                    st.markdown(
                        f"- Xử lý: "
                        f"{error['action']}"
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
                    f"{status['emoji']} "
                    f"**{status['name']}** — "
                    f"{status['meaning']} "
                    f"**Xử lý tiếp:** "
                    f"{status['next_action']}"
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
            "**Không liên quan trực tiếp đến block tiếp theo:** "
            f"{prerequisite_rules['not_required_for_next_block']}"
        )

        st.markdown(
            "**Là điều kiện tiên quyết bắt buộc:** "
            f"{prerequisite_rules['required_for_next_block']}"
        )

        st.markdown(
            "**Lỗ hổng nghiêm trọng:** "
            f"{prerequisite_rules['severe_gap']}"
        )

    with st.expander(
        "🔁 Quy tắc lỗ hổng dai dẳng"
    ):
        st.markdown(persistent_gap_rule)

    with st.expander(
        "📖 Chú thích các màu"
    ):
        st.markdown(
            """
🔴 **Ngày đỏ — ngày 0:** kiểm tra bài cũ hoặc nợ kiến thức và dạy kiến thức mới.

🟠 **Ngày cam — ngày 1:** tự nhớ, chép lại và kiểm tra qua ảnh.

🟡 **Ngày vàng — ngày 3:** đọc lại, làm bài tập, tự giải thích và kiểm tra qua video.

🟢 **Ngày xanh lá — ngày 7:** củng cố, làm bài và chữa trực tiếp online.

🔵 **Ngày xanh dương:** bài kiểm tra chẩn đoán cuối block.

⚫ **Ngày đen:** vá đúng đơn vị kiến thức cần xử lý.

🟣 **Ngày tím:** tổng ôn định kỳ sau mỗi 4 block.
            """
        )

    with st.expander(
        "🟣 Quy tắc ngày tím"
    ):
        st.markdown(
            f"**Mốc:** "
            f"{purple_review_info.get('milestone', '-')}"
        )

        tasks = purple_review_info.get(
            "tasks",
            [],
        )

        if tasks:
            st.markdown("**Cần làm:**")

            for task in tasks:
                st.markdown(f"- {task}")

        priority = purple_review_info.get(
            "priority",
            [],
        )

        if priority:
            st.markdown("**Ưu tiên:**")

            for item in priority:
                st.markdown(f"- {item}")

        st.markdown(
            "**Lưu ý:** "
            f"{purple_review_info.get('note', '-')}"
        )