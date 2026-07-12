import calendar
from datetime import date

import streamlit as st


def get_event_label(event):
    return f"{event['emoji']} {event['subject']}"


def get_short_subject(subject):
    mapping = {
        "Tiếng Anh": "Anh",
        "Toán": "Toán",
        "Vật lý": "Lý",
    }
    return mapping.get(subject, subject)


def build_day_button_label(day_number, events, is_today=False):
    lines = []
    if is_today:
        lines.append(f"✓ • {day_number}")
    else:
        lines.append(str(day_number))

    for event in events:
        emoji = event.get("emoji", "")
        subject = get_short_subject(event.get("subject", ""))
        lines.append(f"{emoji} {subject}")

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


def inject_dashboard_css():
    st.markdown(
        """
        <style>
        :root {
            --bg-page: #f6f7fb;
            --bg-card: rgba(255, 255, 255, 0.94);
            --text-main: #172033;
            --text-soft: #687086;
            --border: rgba(23, 32, 51, 0.09);
            --shadow: 0 14px 40px rgba(23, 32, 51, 0.08);
            --radius-lg: 22px;
            --radius-md: 16px;
            --radius-sm: 12px;
            --accent: #6571d8;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(101, 113, 216, 0.12), transparent 28rem),
                var(--bg-page);
            color: var(--text-main);
        }

        .block-container {
            max-width: 1600px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }

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
            font-size: clamp(2rem, 4vw, 3.25rem);
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: var(--text-main);
        }

        .app-header p {
            margin-top: 0.55rem;
            color: var(--text-soft);
            font-size: 1rem;
        }

        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            padding: 0.95rem 1rem;
            box-sizing: border-box;
            width: 100%;
            height: auto;
            min-height: 0;
            overflow-wrap: anywhere;
        }

        .section-label {
            font-size: 0.74rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--text-soft);
            margin-bottom: 0.4rem;
        }

        .hero-date {
            font-size: clamp(1.3rem, 2.4vw, 1.85rem);
            font-weight: 750;
            letter-spacing: -0.025em;
            color: var(--text-main);
            margin-top: 0.35rem;
        }

        .hero-block {
            display: inline-block;
            margin-top: 0.5rem;
            padding: 0.42rem 0.7rem;
            border-radius: 999px;
            background: rgba(101, 113, 216, 0.1);
            color: var(--accent);
            font-size: 0.88rem;
            font-weight: 700;
        }

        .hero-list {
            margin: 0.8rem 0 0;
            padding-left: 1rem;
            color: var(--text-main);
        }

        .hero-list li {
            margin-bottom: 0.45rem;
        }

        .stat-card {
            background: #eef0f7;
            border: 1px solid rgba(23, 32, 51, 0.06);
            border-radius: var(--radius-md);
            padding: 0.8rem 0.9rem;
            min-height: 92px;
            box-sizing: border-box;
            overflow-wrap: anywhere;
        }

        .stat-label {
            color: var(--text-soft);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .stat-value {
            margin-top: 0.4rem;
            font-size: 1.2rem;
            font-weight: 750;
            letter-spacing: -0.02em;
            color: var(--text-main);
        }

        .calendar-header {
            text-align: center;
            font-weight: 700;
            padding: 0.55rem 0.15rem;
            border-radius: 0.7rem;
            background: rgba(128, 128, 128, 0.12);
            margin-bottom: 0.28rem;
            color: var(--text-main);
        }

        div[data-testid="stButton"] > button {
            width: 100%;
            min-height: 0;
            border-radius: 14px;
            border: 1px solid rgba(23, 32, 51, 0.12);
            background: #ffffff;
            color: var(--text-main);
            text-align: left;
            align-items: flex-start;
            justify-content: flex-start;
            padding: 0.55rem 0.6rem;
            white-space: pre-wrap;
            line-height: 1.25;
            box-sizing: border-box;
            transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
        }

        div[data-testid="stButton"] > button:hover {
            border-color: rgba(87, 105, 255, 0.45);
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(23, 32, 51, 0.08);
        }

        div[data-testid="stButton"] > button:active {
            transform: scale(0.985);
        }

        .calendar-day-cell {
            background: #ffffff;
            color: var(--text-main);
            border: 1px solid rgba(23, 32, 51, 0.12);
        }

        .calendar-day-cell.is-today {
            border-color: #6571d8;
            box-shadow: 0 0 0 3px rgba(101, 113, 216, 0.12);
        }

        .calendar-day-cell.is-selected {
            border-width: 2px;
            border-color: #6571d8;
            box-shadow: 0 0 0 3px rgba(101, 113, 216, 0.12);
        }

        .calendar-day-cell.is-placeholder {
            background: #f1f3f8;
            border-style: dashed;
            color: #7b8498;
            border-color: rgba(23, 32, 51, 0.09);
        }

        .calendar-day-cell.is-placeholder:hover {
            box-shadow: none;
            transform: none;
        }

        .day-chip {
            display: inline-block;
            margin-top: 0.32rem;
            padding: 0.2rem 0.38rem;
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: #33415c;
            background: rgba(101, 113, 216, 0.08);
            width: fit-content;
            max-width: 100%;
            white-space: normal;
            overflow-wrap: anywhere;
        }

        .day-chip.red { background: rgba(234, 83, 83, 0.12); color: #b43f3f; }
        .day-chip.orange { background: rgba(241, 139, 73, 0.15); color: #b15c1f; }
        .day-chip.yellow { background: rgba(238, 204, 82, 0.2); color: #8f6e14; }
        .day-chip.green { background: rgba(80, 176, 106, 0.15); color: #2f6d3d; }
        .day-chip.blue { background: rgba(77, 133, 219, 0.14); color: #2f5a9a; }
        .day-chip.black { background: rgba(88, 96, 106, 0.16); color: #424a54; }
        .day-chip.purple { background: rgba(142, 103, 202, 0.15); color: #6c3ea3; }
        .day-chip.neutral { background: rgba(101, 113, 216, 0.08); }

        .day-empty {
            min-height: 112px;
            border-radius: 16px;
            border: 1px dashed rgba(23, 32, 51, 0.08);
            background: rgba(255, 255, 255, 0.4);
        }

        .detail-card {
            background: #ffffff;
            border: 1px solid rgba(23, 32, 51, 0.08);
            border-radius: 16px;
            padding: 0.85rem 0.95rem;
            margin-bottom: 0.8rem;
            box-sizing: border-box;
            overflow-wrap: anywhere;
        }

        .detail-title {
            font-size: 1.03rem;
            font-weight: 750;
            margin-bottom: 0.2rem;
        }

        .detail-meta {
            color: var(--text-soft);
            font-size: 0.9rem;
            margin-bottom: 0.65rem;
        }

        .detail-pill {
            display: inline-flex;
            align-items: center;
            width: fit-content;
            max-width: 100%;
            min-height: 32px;
            padding: 0.32rem 0.65rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 700;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            background: #eef0f7;
            color: #2f3853;
            box-sizing: border-box;
            white-space: normal;
            overflow-wrap: anywhere;
        }

        @media (max-width: 1100px) {
            .block-container {
                padding-left: 0.8rem;
                padding-right: 0.8rem;
            }
        }

        @media (max-width: 820px) {
            .block-container {
                padding-left: 0.45rem;
                padding-right: 0.45rem;
            }

            .app-header h1 {
                font-size: 2rem;
            }

            div[data-testid="stButton"] > button {
                padding: 0.5rem 0.55rem;
            }
        }

        @media (max-width: 600px) {
            .app-header p {
                font-size: 0.92rem;
            }

            div[data-testid="stButton"] > button {
                padding: 0.45rem 0.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_app_header():
    st.markdown(
        """
        <div class="app-header">
            <div class="app-eyebrow">STUDY CALENDAR</div>
            <h1>Lịch học của L</h1>
            <p>Học đúng nhịp · Nhớ lâu hơn · Chỉ sửa đúng phần còn yếu</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_today_hero(today, events, start_date, block_number, format_vietnamese_date):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Hôm nay</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-date">{format_vietnamese_date(today)}</div>', unsafe_allow_html=True)

    if block_number is not None:
        st.markdown(f'<div class="hero-block">Block {block_number}</div>', unsafe_allow_html=True)

    if today < start_date:
        st.info(f"Chương trình bắt đầu từ {start_date.strftime('%d/%m/%Y')}.")
    elif not events:
        st.info("Hôm nay không có nhiệm vụ học tập.")
    else:
        st.markdown('<ul class="hero-list">', unsafe_allow_html=True)
        for event in events:
            st.markdown(
                f"<li><strong>{event['emoji']} {event['full_subject']}</strong> · {event['stage']} · {event['milestone']}</li>",
                unsafe_allow_html=True,
            )
        st.markdown('</ul>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_quick_stats(block_number, today_events_count, selected_date, next_milestone):
    cols = st.columns(4)
    with cols[0]:
        st.markdown(
            '<div class="stat-card"><div class="stat-label">Block hiện tại</div><div class="stat-value">' + str(block_number or "—") + '</div></div>',
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            '<div class="stat-card"><div class="stat-label">Nhiệm vụ hôm nay</div><div class="stat-value">' + str(today_events_count) + ' nhiệm vụ</div></div>',
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            '<div class="stat-card"><div class="stat-label">Ngày đã chọn</div><div class="stat-value">' + selected_date.strftime('%d/%m/%Y') + '</div></div>',
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            '<div class="stat-card"><div class="stat-label">Mốc tiếp theo</div><div class="stat-value">' + next_milestone + '</div></div>',
            unsafe_allow_html=True,
        )


def render_month_toolbar(previous_month, next_month, go_to_today, go_to_purple_week):
    top = st.columns([1, 2, 1])
    with top[0]:
        st.button("◀", on_click=previous_month, use_container_width=True, key="prev_month")
    with top[1]:
        st.markdown('<div class="section-label" style="text-align:center;">Tháng đang xem</div>', unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:1.05rem;font-weight:700;text-align:center;'>Tháng {st.session_state.view_month} · {st.session_state.view_year}</div>",
            unsafe_allow_html=True,
        )
    with top[2]:
        st.button("▶", on_click=next_month, use_container_width=True, key="next_month")

    toolbar_cols = st.columns([1, 1.25, 1, 1.25])
    with toolbar_cols[0]:
        st.button("Hôm nay", on_click=go_to_today, use_container_width=True)
    with toolbar_cols[1]:
        st.button("Tuần tím đầu tiên", on_click=go_to_purple_week, use_container_width=True)
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
        year_options = list(range(min(st.session_state.view_year, current_view_year - 5), max(st.session_state.view_year + 20, current_view_year + 5) + 1))
        selected_year = st.selectbox("Năm", options=year_options, index=year_options.index(current_view_year), key="year_selector")

    if selected_month != st.session_state.view_month or selected_year != st.session_state.view_year:
        st.session_state.view_month = selected_month
        st.session_state.view_year = selected_year
        st.rerun()


def render_calendar_grid(year, month, schedule, today, selected_date, select_date):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Lịch tháng</div>', unsafe_allow_html=True)

    header_columns = st.columns(7)
    for index, header in enumerate(["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]):
        with header_columns[index]:
            st.markdown(f"<div class='calendar-header'>{header}</div>", unsafe_allow_html=True)

    cal = calendar.Calendar(firstweekday=0)
    weeks = cal.monthdatescalendar(year, month)

    for week in weeks:
        columns = st.columns(7)
        for index, current_date in enumerate(week):
            with columns[index]:
                if current_date.month != month:
                    st.markdown('<div class="day-empty"></div>', unsafe_allow_html=True)
                    continue

                events = schedule.get(current_date, [])
                is_today = current_date == today
                is_selected = current_date == selected_date
                button_label = build_day_button_label(current_date.day, events[:2], is_today=is_today)
                if len(events) > 2:
                    button_label = f"{button_label}\n+{len(events) - 2} khác"

                if is_today:
                    button_label = f"{button_label}\nHôm nay"
                if is_selected:
                    button_label = f"{button_label}\nĐang chọn"

                st.button(
                    button_label,
                    key=f"day_{current_date.isoformat()}",
                    on_click=select_date,
                    args=(current_date,),
                    use_container_width=True,
                )

    st.markdown('</div>', unsafe_allow_html=True)


def render_selected_day_details(selected_date, selected_events, block_number, format_vietnamese_date, get_day_type_details, error_types, repair_statuses):
    st.markdown('<div class="glass-card" style="margin-top:1rem;">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Chi tiết ngày đã chọn</div>', unsafe_allow_html=True)
    st.markdown(f"<div class='hero-date'>{format_vietnamese_date(selected_date)}</div>", unsafe_allow_html=True)
    if block_number is not None:
        st.markdown(f'<div class="hero-block">Block {block_number} · {len(selected_events)} nhiệm vụ</div>', unsafe_allow_html=True)

    if not selected_events:
        st.info("Không có nhiệm vụ học tập trong ngày này.")
    else:
        for event in selected_events:
            st.markdown(f"<div class='detail-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-title'>{event['emoji']} {event['full_subject']} · {event['stage']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-meta'>Mốc: {event['milestone']}</div>", unsafe_allow_html=True)
            detail_map = {
                "study_mode": event.get("study_mode", "-"),
                "start_time": event.get("start_time", "-"),
                "duration": event.get("duration", "-"),
            }
            if not detail_map["study_mode"] or detail_map["study_mode"] == "-":
                detail_map = get_day_type_details(event.get("stage", ""))
            st.markdown(f"<div class='detail-pill'>Hình thức học: {detail_map['study_mode']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-pill'>Giờ bắt đầu: {detail_map['start_time']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-pill'>Thời lượng: {detail_map['duration']}</div>", unsafe_allow_html=True)
            if event.get("tasks"):
                st.markdown("**Cần làm:**")
                for task in event["tasks"]:
                    st.markdown(f"- {task}")
            st.markdown(f"**Hình thức kiểm tra:** {event.get('check_method', '-')}\n\n**Mục tiêu:** {event.get('goal', '-')}")
            if event.get("notes"):
                st.markdown("**Lưu ý:**")
                for note in event["notes"]:
                    st.markdown(f"- {note}")
            if event.get("type") == "test":
                with st.expander("Xem cách phân loại lỗi sau kiểm tra"):
                    for error in error_types:
                        st.markdown(f"**{error['code']}. {error['name']}**")
                        st.markdown(f"- Biểu hiện: {error['symptom']}")
                        st.markdown(f"- Xử lý: {error['action']}")
            if event.get("type") == "repair":
                priority_order = event.get("priority_order", [])
                if priority_order:
                    st.markdown("**Thứ tự ưu tiên xử lý:**")
                    for number, item in enumerate(priority_order, start=1):
                        st.markdown(f"{number}. {item}")
                st.markdown("**Trạng thái sau khi xử lý:**")
                for status in repair_statuses:
                    st.markdown(f"{status['emoji']} **{status['name']}** — {status['meaning']} **Xử lý tiếp:** {status['next_action']}")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_learning_rule_sections(prerequisite_rules, persistent_gap_rule, purple_review_info):
    st.divider()
    with st.expander("🧠 Quy tắc xử lý kiến thức tiên quyết"):
        st.markdown(f"**Không liên quan trực tiếp đến block tiếp theo:** {prerequisite_rules['not_required_for_next_block']}")
        st.markdown(f"**Là điều kiện tiên quyết bắt buộc:** {prerequisite_rules['required_for_next_block']}")
        st.markdown(f"**Lỗ hổng nghiêm trọng:** {prerequisite_rules['severe_gap']}")

    with st.expander("🔁 Quy tắc lỗ hổng dai dẳng"):
        st.markdown(persistent_gap_rule)

    with st.expander("📖 Chú thích các màu"):
        st.markdown(
            """
            🔴 Ngày đỏ — ngày 0: kiểm tra bài cũ hoặc nợ kiến thức và dạy kiến thức mới.

            🟠 Ngày cam — ngày 1: tự nhớ, chép lại và kiểm tra qua ảnh.

            🟡 Ngày vàng — ngày 3: đọc lại, làm bài tập, tự giải thích và kiểm tra qua video.

            🟢 Ngày xanh lá — ngày 7: củng cố, làm bài và chữa trực tiếp online.

            🔵 Ngày xanh dương: bài kiểm tra chẩn đoán cuối block.

            ⚫ Ngày đen: vá đúng đơn vị kiến thức cần xử lý.

            🟣 Ngày tím: tổng ôn định kỳ sau mỗi 4 block.
            """
        )

    with st.expander("🟣 Quy tắc ngày tím"):
        st.markdown(f"**Mốc:** {purple_review_info['milestone']}")
        st.markdown("**Cần làm:**")
        for task in purple_review_info["tasks"]:
            st.markdown(f"- {task}")
        st.markdown("**Ưu tiên:**")
        for item in purple_review_info["priority"]:
            st.markdown(f"- {item}")
        st.markdown(f"**Lưu ý:** {purple_review_info['note']}")
