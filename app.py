import calendar
from datetime import date

import streamlit as st

from scheduler import (
    CALENDAR_HEADERS,
    START_DATE,
    format_vietnamese_date,
    generate_schedule,
    get_block_number,
)

st.set_page_config(
    page_title="Lịch học của L",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1500px; padding-top: 1.2rem; padding-bottom: 3rem; }
    .calendar-header { text-align: center; font-weight: 700; padding: 0.55rem 0.15rem; border-radius: 0.5rem; background: rgba(128, 128, 128, 0.14); margin-bottom: 0.25rem; }
    .today-card { padding: 1rem; border: 1px solid rgba(128, 128, 128, 0.3); border-radius: 0.8rem; margin-bottom: 1rem; }
    .detail-card { padding: 1rem; border: 1px solid rgba(128, 128, 128, 0.3); border-radius: 0.8rem; margin: 0.7rem 0; }
    div[data-testid="stButton"] button { min-height: 3rem; white-space: normal; }
    @media (max-width: 900px) { .block-container { padding-left: 0.6rem; padding-right: 0.6rem; } .calendar-header { font-size: 0.75rem; } div[data-testid="stButton"] button { font-size: 0.78rem; padding-left: 0.2rem; padding-right: 0.2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 Lịch học của L")

today = date.today()

if "view_year" not in st.session_state:
    st.session_state.view_year = today.year

if "view_month" not in st.session_state:
    st.session_state.view_month = today.month

if "selected_date" not in st.session_state:
    st.session_state.selected_date = today if today >= START_DATE else START_DATE


def previous_month():
    if st.session_state.view_month == 1:
        st.session_state.view_month = 12
        st.session_state.view_year -= 1
    else:
        st.session_state.view_month -= 1


def next_month():
    if st.session_state.view_month == 12:
        st.session_state.view_month = 1
        st.session_state.view_year += 1
    else:
        st.session_state.view_month += 1


def go_to_today():
    st.session_state.view_year = today.year
    st.session_state.view_month = today.month
    st.session_state.selected_date = today


def select_date(target_date):
    st.session_state.selected_date = target_date


with st.container():
    st.subheader("Hôm nay")
    st.markdown(f"**{format_vietnamese_date(today)}**")

    today_schedule = generate_schedule(today)
    today_events = today_schedule.get(today, [])

    if today < START_DATE:
        st.info(f"Chương trình học chưa bắt đầu. Ngày bắt đầu là {START_DATE.strftime('%d/%m/%Y')}.")
    elif not today_events:
        st.info("Hôm nay không có nhiệm vụ học tập.")
    else:
        for event in today_events:
            st.markdown(f"{event['emoji']} **{event['subject']}** — {event['stage']} · {event['milestone']}")

st.divider()

nav_left, nav_center, nav_right = st.columns([1, 1, 1])
with nav_left:
    st.button("◀ Tháng trước", on_click=previous_month, use_container_width=True)
with nav_center:
    st.button("Hôm nay", on_click=go_to_today, use_container_width=True)
with nav_right:
    st.button("Tháng sau ▶", on_click=next_month, use_container_width=True)

selector_left, selector_right = st.columns(2)
with selector_left:
    selected_month = st.selectbox(
        "Chọn tháng",
        options=list(range(1, 13)),
        index=st.session_state.view_month - 1,
        format_func=lambda value: f"Tháng {value}",
    )
with selector_right:
    current_view_year = st.session_state.view_year
    year_options = list(range(min(2026, current_view_year - 5), max(today.year + 20, current_view_year + 5) + 1))
    selected_year = st.selectbox("Chọn năm", options=year_options, index=year_options.index(current_view_year))

if selected_month != st.session_state.view_month or selected_year != st.session_state.view_year:
    st.session_state.view_month = selected_month
    st.session_state.view_year = selected_year
    st.rerun()

year = st.session_state.view_year
month = st.session_state.view_month
last_day = calendar.monthrange(year, month)[1]
month_end = date(year, month, last_day)
schedule = generate_schedule(month_end)

st.markdown(f"<h2 style='text-align:center;'>Tháng {month}/{year}</h2>", unsafe_allow_html=True)

header_columns = st.columns(7)
for index, header in enumerate(CALENDAR_HEADERS):
    with header_columns[index]:
        st.markdown(f"<div class='calendar-header'>{header}</div>", unsafe_allow_html=True)

cal = calendar.Calendar(firstweekday=0)
weeks = cal.monthdatescalendar(year, month)
for week in weeks:
    columns = st.columns(7)
    for index, current_date in enumerate(week):
        with columns[index]:
            if current_date.month != month:
                st.markdown("&nbsp;", unsafe_allow_html=True)
                continue

            events = schedule.get(current_date, [])
            labels = [f"{event['emoji']} {event['subject']}" for event in events]
            button_text = str(current_date.day)
            if labels:
                button_text += "\n" + "\n".join(labels)
            if current_date == today:
                button_text = "● " + button_text
            if current_date == st.session_state.selected_date:
                button_text = "✓ " + button_text

            st.button(
                button_text,
                key=f"day_{current_date.isoformat()}",
                on_click=select_date,
                args=(current_date,),
                use_container_width=True,
            )

st.divider()
selected_date = st.session_state.selected_date
selected_events = generate_schedule(selected_date).get(selected_date, [])

st.subheader("Chi tiết ngày đã chọn")
st.markdown(f"### {format_vietnamese_date(selected_date)}")
block_number = get_block_number(selected_date)
if block_number is not None:
    st.caption(f"Block {block_number} · {len(selected_events)} nhiệm vụ")

if selected_date < START_DATE:
    st.info("Ngày này nằm trước thời điểm bắt đầu chương trình học.")
elif not selected_events:
    st.info("Không có nhiệm vụ học tập trong ngày này.")
else:
    for event in selected_events:
        with st.container(border=True):
            st.markdown(f"### {event['emoji']} {event['full_subject'].upper()} — {event['stage'].upper()}")
            st.markdown(f"**Mốc:** {event['milestone']}")
            st.markdown("**Cần làm:**")
            for task in event["tasks"]:
                st.markdown(f"- {task}")
            st.markdown(f"**Hình thức kiểm tra:** {event['check_method']}")
            st.markdown(f"**Mục tiêu:** {event['goal']}")

st.divider()
with st.expander("📖 Xem chú thích các màu"):
    st.markdown(
        """
        🔴 **Ngày đỏ — Ngày 0:** Kiểm tra bài cũ và dạy kiến thức mới.

        🟠 **Ngày cam — Ngày 1:** Chép lại kiến thức và gửi ảnh kiểm tra.

        🟡 **Ngày vàng — Ngày 3:** Đọc lại, làm bài tập, tự giải thích và quay video.

        🟢 **Ngày xanh lá — Ngày 7:** Ôn tập, làm bài và chữa trực tiếp online.

        🔵 **Ngày xanh dương:** Kiểm tra đánh giá cuối block.

        ⚫ **Ngày đen:** Vá đúng những đơn vị kiến thức chưa đạt.
        """
    )

with st.expander("⚙️ Thông tin hệ thống"):
    st.markdown(
        f"""
        **Ngày bắt đầu:** {START_DATE.strftime('%d/%m/%Y')}

        **Độ dài mỗi block:** 14 ngày

        **Thứ tự môn:** Tiếng Anh → Toán → Vật lý

        **Chu kỳ:** Ngày 0 → Ngày 1 → Ngày 3 → Ngày 7 → Kiểm tra cuối block → Vá lỗi
        """
    )
