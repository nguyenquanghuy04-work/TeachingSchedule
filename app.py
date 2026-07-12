import calendar
import importlib
import sys
import types
from datetime import date

from scheduler import get_current_vietnam_date
from pathlib import Path

import streamlit as st


def load_scheduler_module():
    root = Path(__file__).resolve().parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    try:
        return importlib.import_module("scheduler")
    except Exception:
        return types.SimpleNamespace()


def get_scheduler_symbol(module, name, default=None):
    return getattr(module, name, default)


scheduler = load_scheduler_module()


def _format_vietnamese_date(value):
    weekday_names = [
        "Thứ Hai",
        "Thứ Ba",
        "Thứ Tư",
        "Thứ Năm",
        "Thứ Sáu",
        "Thứ Bảy",
        "Chủ nhật",
    ]
    weekday = weekday_names[value.weekday()]
    return f"{weekday}, {value.strftime('%d/%m/%Y')}"


def _get_block_number(target_date):
    if target_date < START_DATE:
        return None
    return (target_date - START_DATE).days // BLOCK_LENGTH + 1


START_DATE = get_scheduler_symbol(scheduler, "START_DATE", date(2026, 7, 13))
BLOCK_LENGTH = get_scheduler_symbol(scheduler, "BLOCK_LENGTH", 14)
SUBJECTS = get_scheduler_symbol(
    scheduler,
    "SUBJECTS",
    [
        {"name": "Tiếng Anh", "short": "Anh", "offset": 0},
        {"name": "Toán", "short": "Toán", "offset": 2},
        {"name": "Vật lý", "short": "Lý", "offset": 4},
    ],
)
ERROR_TYPES = get_scheduler_symbol(
    scheduler,
    "ERROR_TYPES",
    [
        {
            "code": "A",
            "name": "Chưa hiểu",
            "symptom": "Không hiểu khái niệm hoặc không biết cách giải.",
            "action": "Đưa vào ngày đen, ưu tiên cao.",
        },
        {
            "code": "B",
            "name": "Quên kiến thức",
            "symptom": "Trước đây làm được nhưng hiện tại không nhớ.",
            "action": "Ôn nhanh trong ngày đen.",
        },
        {
            "code": "C",
            "name": "Áp dụng sai",
            "symptom": "Biết kiến thức nhưng chọn sai phương pháp hoặc sai quy trình.",
            "action": "Làm thêm bài tương tự.",
        },
        {
            "code": "D",
            "name": "Bất cẩn",
            "symptom": "Tính nhầm, sai dấu, đọc thiếu đề hoặc lỗi tương tự.",
            "action": "Ghi nhận; chưa cần ôn lại nếu chỉ xảy ra một lần.",
        },
    ],
)
REPAIR_STATUSES = get_scheduler_symbol(
    scheduler,
    "REPAIR_STATUSES",
    [
        {
            "emoji": "🟢",
            "name": "Đã vá",
            "meaning": "Hiểu và tự làm được bài tương tự.",
            "next_action": "Kết thúc.",
        },
        {
            "emoji": "🟡",
            "name": "Tạm ổn",
            "meaning": "Đã hiểu lại nhưng chưa chắc chắn.",
            "next_action": "Đưa vào kiểm tra bài cũ ngày đỏ của block sau.",
        },
        {
            "emoji": "🔴",
            "name": "Chưa vá được",
            "meaning": "Vẫn chưa hiểu hoặc chưa thể tự làm.",
            "next_action": "Bắt buộc đưa vào kiểm tra bài cũ ngày đỏ của block sau.",
        },
    ],
)
PREREQUISITE_RULES = get_scheduler_symbol(
    scheduler,
    "PREREQUISITE_RULES",
    {
        "not_required_for_next_block": "Tiếp tục học block mới bình thường.",
        "required_for_next_block": "Ưu tiên xử lý kiến thức đó ở đầu ngày đỏ.",
        "severe_gap": "Cân nhắc điều chỉnh nội dung block nếu lỗ hổng quá nghiêm trọng.",
    },
)
PERSISTENT_GAP_RULE = get_scheduler_symbol(
    scheduler,
    "PERSISTENT_GAP_RULE",
    "Nếu một đơn vị kiến thức vẫn chưa đạt sau nhiều lần xử lý, đổi cách tiếp cận.",
)
PURPLE_REVIEW_INFO = get_scheduler_symbol(
    scheduler,
    "PURPLE_REVIEW_INFO",
    {
        "milestone": "Tổng ôn định kỳ 2 tháng",
        "tasks": [],
        "priority": [],
        "note": "Chưa tự động chèn vào calendar.",
    },
)
CALENDAR_HEADERS = get_scheduler_symbol(
    scheduler,
    "CALENDAR_HEADERS",
    ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"],
)
format_vietnamese_date = get_scheduler_symbol(
    scheduler,
    "format_vietnamese_date",
    _format_vietnamese_date,
)
get_block_number = get_scheduler_symbol(
    scheduler,
    "get_block_number",
    _get_block_number,
)
generate_schedule = get_scheduler_symbol(
    scheduler,
    "generate_schedule",
    lambda end_date: {},
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Lịch học của L",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SESSION STATE
# ============================================================

today = get_current_vietnam_date()

if "view_year" not in st.session_state:
    st.session_state.view_year = START_DATE.year

if "view_month" not in st.session_state:
    st.session_state.view_month = START_DATE.month

if "selected_date" not in st.session_state:
    st.session_state.selected_date = START_DATE


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

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    .calendar-header {
        text-align: center;
        font-weight: 700;
        padding: 0.55rem 0.15rem;
        border-radius: 0.5rem;
        background: rgba(128, 128, 128, 0.14);
        margin-bottom: 0.25rem;
    }

    div[data-testid="stButton"] button {
        min-height: 3.4rem;
        white-space: pre-line;
        line-height: 1.25;
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }

        .calendar-header {
            font-size: 0.72rem;
        }

        div[data-testid="stButton"] button {
            font-size: 0.76rem;
            padding-left: 0.15rem;
            padding-right: 0.15rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# TITLE
# ============================================================

st.title("📚 Lịch học của L")

st.caption(
    "Học theo block cố định · Chẩn đoán chính xác từng lỗ hổng · "
    "Chỉ sửa đúng phần còn yếu · Không reset toàn bộ chương vì một lỗi nhỏ"
)

# ============================================================
# TODAY
# ============================================================

st.subheader("📌 Hôm nay")

today_schedule = generate_schedule(max(today, START_DATE))
today_events = today_schedule.get(today, [])

st.markdown(f"**{format_vietnamese_date(today)}**")

if today < START_DATE:
    st.info(
        "Chương trình học chưa bắt đầu. "
        f"Ngày bắt đầu là {START_DATE.strftime('%d/%m/%Y')}."
    )
elif not today_events:
    st.info("Hôm nay không có nhiệm vụ học tập.")
else:
    for event in today_events:
        st.markdown(
            f"{event['emoji']} **{event['subject']}** — "
            f"{event['stage']} · {event['milestone']}"
        )

# ============================================================
# NAVIGATION
# ============================================================

st.divider()

nav_left, nav_center, nav_right = st.columns(3)

with nav_left:
    st.button(
        "◀ Tháng trước",
        on_click=previous_month,
        use_container_width=True,
    )

with nav_center:
    st.button(
        "Hôm nay",
        on_click=go_to_today,
        use_container_width=True,
    )

with nav_right:
    st.button(
        "Tháng sau ▶",
        on_click=next_month,
        use_container_width=True,
    )

# ============================================================
# DIRECT MONTH / YEAR SELECTOR
# ============================================================

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

    year_options = list(
        range(
            min(START_DATE.year, current_view_year - 5),
            max(today.year + 20, current_view_year + 5) + 1,
        )
    )

    selected_year = st.selectbox(
        "Chọn năm",
        options=year_options,
        index=year_options.index(current_view_year),
    )

if (
    selected_month != st.session_state.view_month
    or selected_year != st.session_state.view_year
):
    st.session_state.view_month = selected_month
    st.session_state.view_year = selected_year
    st.rerun()

# ============================================================
# CURRENT MONTH
# ============================================================

year = st.session_state.view_year
month = st.session_state.view_month

last_day = calendar.monthrange(year, month)[1]
month_end = date(year, month, last_day)

schedule = generate_schedule(max(month_end, today, START_DATE))

st.markdown(
    f"<h2 style='text-align:center;'>Tháng {month}/{year}</h2>",
    unsafe_allow_html=True,
)

# ============================================================
# CALENDAR HEADER
# ============================================================

header_columns = st.columns(7)

for index, header in enumerate(CALENDAR_HEADERS):
    with header_columns[index]:
        st.markdown(
            f"<div class='calendar-header'>{header}</div>",
            unsafe_allow_html=True,
        )

# ============================================================
# CALENDAR GRID
# ============================================================

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

            labels = [
                f"{event['emoji']} {event['subject']}"
                for event in events
            ]

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

# ============================================================
# SELECTED DATE DETAILS
# ============================================================

st.divider()

selected_date = st.session_state.selected_date
detail_schedule = generate_schedule(max(selected_date, START_DATE))
selected_events = detail_schedule.get(selected_date, [])

st.subheader("📋 Chi tiết ngày đã chọn")
st.markdown(f"### {format_vietnamese_date(selected_date)}")

block_number = get_block_number(selected_date)

if block_number is not None:
    st.caption(
        f"Block {block_number} · {len(selected_events)} nhiệm vụ"
    )

if selected_date < START_DATE:
    st.info(
        "Ngày này nằm trước thời điểm bắt đầu chương trình học."
    )

elif not selected_events:
    st.info(
        "Không có nhiệm vụ học tập trong ngày này."
    )

else:
    for event in selected_events:
        with st.container(border=True):

            st.markdown(
                f"### {event['emoji']} "
                f"{event['full_subject'].upper()} — "
                f"{event['stage'].upper()}"
            )

            st.markdown(f"**Mốc:** {event['milestone']}")

            st.markdown(
                f"**Hình thức học:** {event.get('study_mode', '-')}"
            )
            st.markdown(
                f"**Giờ bắt đầu:** {event.get('start_time', '-')}"
            )
            st.markdown(
                f"**Thời lượng:** {event.get('duration', '-')}"
            )

            st.markdown("**Cần làm:**")

            for task in event["tasks"]:
                st.markdown(f"- {task}")

            st.markdown(
                f"**Hình thức kiểm tra:** "
                f"{event['check_method']}"
            )

            st.markdown(
                f"**Mục tiêu:** {event['goal']}"
            )

            notes = event.get("notes", [])

            if notes:
                st.markdown("**Lưu ý:**")
                for note in notes:
                    st.markdown(f"- {note}")

            if event["type"] == "test":
                with st.expander(
                    "Xem cách phân loại lỗi sau kiểm tra"
                ):
                    for error in ERROR_TYPES:
                        st.markdown(
                            f"**{error['code']}. {error['name']}**"
                        )
                        st.markdown(
                            f"- Biểu hiện: {error['symptom']}"
                        )
                        st.markdown(
                            f"- Xử lý: {error['action']}"
                        )

            if event["type"] == "repair":
                priority_order = event.get("priority_order", [])

                if priority_order:
                    st.markdown("**Thứ tự ưu tiên xử lý:**")
                    for number, item in enumerate(
                        priority_order,
                        start=1,
                    ):
                        st.markdown(f"{number}. {item}")

                st.markdown("**Trạng thái sau khi xử lý:**")

                for status in REPAIR_STATUSES:
                    st.markdown(
                        f"{status['emoji']} "
                        f"**{status['name']}** — "
                        f"{status['meaning']} "
                        f"**Xử lý tiếp:** {status['next_action']}"
                    )

# ============================================================
# LEARNING RULES
# ============================================================

st.divider()

with st.expander("🧠 Quy tắc xử lý kiến thức tiên quyết"):

    st.markdown(
        f"**Không liên quan trực tiếp đến block tiếp theo:** "
        f"{PREREQUISITE_RULES['not_required_for_next_block']}"
    )

    st.markdown(
        f"**Là điều kiện tiên quyết bắt buộc:** "
        f"{PREREQUISITE_RULES['required_for_next_block']}"
    )

    st.markdown(
        f"**Lỗ hổng nghiêm trọng:** "
        f"{PREREQUISITE_RULES['severe_gap']}"
    )

with st.expander("🔁 Quy tắc lỗ hổng dai dẳng"):
    st.markdown(PERSISTENT_GAP_RULE)

# ============================================================
# LEGEND
# ============================================================

with st.expander("📖 Chú thích các màu"):

    st.markdown(
        """
🔴 **Ngày đỏ — Ngày 0:**  
Kiểm tra bài cũ hoặc nợ kiến thức cần thiết và dạy kiến thức mới.

🟠 **Ngày cam — Ngày 1:**  
Tái hiện kiến thức lần đầu, chép lại và kiểm tra qua ảnh.

🟡 **Ngày vàng — Ngày 3:**  
Đọc lại, làm bài tập, tự giải thích và kiểm tra qua video.

🟢 **Ngày xanh lá — Ngày 7:**  
Củng cố, làm bài và chữa trực tiếp online. Đây chưa phải mốc quyết định đạt hay chưa đạt.

🔵 **Ngày xanh dương:**  
Kiểm tra chẩn đoán cuối block theo từng đơn vị kiến thức. Không dùng điểm tổng để tự động quyết định pass/fail toàn block hoặc học lại toàn bộ chương.

⚫ **Ngày đen:**  
Vá đúng những đơn vị kiến thức cần xử lý. Không học lại toàn bộ chương nếu không cần thiết.

🟣 **Ngày tím:**  
Tổng ôn định kỳ 2 tháng. Chưa tự động chèn vào calendar vì chưa có ngày bắt đầu chu kỳ cụ thể.
        """
    )

# ============================================================
# PURPLE REVIEW
# ============================================================

with st.expander("🟣 Quy tắc ngày tím — Tổng ôn định kỳ"):

    st.markdown(
        f"**Mốc:** {PURPLE_REVIEW_INFO['milestone']}"
    )

    st.markdown("**Cần làm:**")

    for task in PURPLE_REVIEW_INFO["tasks"]:
        st.markdown(f"- {task}")

    st.markdown("**Ưu tiên:**")

    for item in PURPLE_REVIEW_INFO["priority"]:
        st.markdown(f"- {item}")

    st.markdown(
        f"**Lưu ý:** {PURPLE_REVIEW_INFO['note']}"
    )

# ============================================================
# SYSTEM INFO
# ============================================================

with st.expander("⚙️ Thông tin hệ thống"):

    subject_order = " → ".join(
        subject["name"] for subject in SUBJECTS
    )

    st.markdown(
        f"""
**Ngày bắt đầu:** {START_DATE.strftime('%d/%m/%Y')}

**Độ dài mỗi block:** {BLOCK_LENGTH} ngày

**Thứ tự môn:** {subject_order}

**Chu kỳ:** Ngày 0 → Ngày 1 → Ngày 3 → Ngày 7 → Kiểm tra chẩn đoán cuối block → Vá đúng đơn vị kiến thức cần xử lý

**Nguyên tắc trung tâm:** Không reset toàn bộ chương vì một lỗi nhỏ hoặc chỉ vì điểm tổng thấp. Chỉ xử lý đúng những đơn vị kiến thức còn yếu và tiếp tục lộ trình.
        """
    )
