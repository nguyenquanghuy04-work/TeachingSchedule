import calendar
import importlib
import sys
import types
from datetime import date, timedelta
from pathlib import Path

import streamlit as st

from scheduler import get_current_vietnam_date
from ui import (
    inject_dashboard_css,
    render_app_header,
    render_calendar_grid,
    render_learning_rule_sections,
    render_month_toolbar,
    render_quick_stats,
    render_selected_day_details,
    render_today_hero,
)


# ============================================================
# SCHEDULER LOADING
# ============================================================

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


# ============================================================
# FALLBACK HELPERS
# ============================================================

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

    return (
        (target_date - START_DATE).days
        // BLOCK_LENGTH
        + 1
    )


# ============================================================
# SCHEDULER CONSTANTS
# ============================================================

START_DATE = get_scheduler_symbol(
    scheduler,
    "START_DATE",
    date(2026, 7, 13),
)

BLOCK_LENGTH = get_scheduler_symbol(
    scheduler,
    "BLOCK_LENGTH",
    14,
)

SUBJECTS = get_scheduler_symbol(
    scheduler,
    "SUBJECTS",
    [
        {
            "name": "Tiếng Anh",
            "short": "Anh",
            "offset": 0,
        },
        {
            "name": "Toán",
            "short": "Toán",
            "offset": 2,
        },
        {
            "name": "Vật lý",
            "short": "Lý",
            "offset": 4,
        },
    ],
)

ERROR_TYPES = get_scheduler_symbol(
    scheduler,
    "ERROR_TYPES",
    [
        {
            "code": "A",
            "name": "Chưa hiểu",
            "symptom": (
                "Không hiểu khái niệm "
                "hoặc không biết cách giải."
            ),
            "action": (
                "Đưa vào ngày đen, ưu tiên cao."
            ),
        },
        {
            "code": "B",
            "name": "Quên kiến thức",
            "symptom": (
                "Trước đây làm được "
                "nhưng hiện tại không nhớ."
            ),
            "action": (
                "Ôn nhanh trong ngày đen."
            ),
        },
        {
            "code": "C",
            "name": "Áp dụng sai",
            "symptom": (
                "Biết kiến thức nhưng chọn sai "
                "phương pháp hoặc sai quy trình."
            ),
            "action": (
                "Làm thêm bài tương tự."
            ),
        },
        {
            "code": "D",
            "name": "Bất cẩn",
            "symptom": (
                "Tính nhầm, sai dấu, đọc thiếu đề "
                "hoặc lỗi tương tự."
            ),
            "action": (
                "Ghi nhận; chưa cần ôn lại "
                "nếu chỉ xảy ra một lần."
            ),
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
            "meaning": (
                "Hiểu và tự làm được bài tương tự."
            ),
            "next_action": "Kết thúc.",
        },
        {
            "emoji": "🟡",
            "name": "Tạm ổn",
            "meaning": (
                "Đã hiểu lại nhưng chưa chắc chắn."
            ),
            "next_action": (
                "Đưa vào kiểm tra bài cũ "
                "ngày đỏ của block sau."
            ),
        },
        {
            "emoji": "🔴",
            "name": "Chưa vá được",
            "meaning": (
                "Vẫn chưa hiểu "
                "hoặc chưa thể tự làm."
            ),
            "next_action": (
                "Bắt buộc đưa vào kiểm tra bài cũ "
                "ngày đỏ của block sau."
            ),
        },
    ],
)

PREREQUISITE_RULES = get_scheduler_symbol(
    scheduler,
    "PREREQUISITE_RULES",
    {
        "not_required_for_next_block": (
            "Tiếp tục học block mới bình thường."
        ),
        "required_for_next_block": (
            "Ưu tiên xử lý kiến thức đó "
            "ở đầu ngày đỏ."
        ),
        "severe_gap": (
            "Cân nhắc điều chỉnh nội dung block "
            "nếu lỗ hổng quá nghiêm trọng."
        ),
    },
)

PERSISTENT_GAP_RULE = get_scheduler_symbol(
    scheduler,
    "PERSISTENT_GAP_RULE",
    (
        "Nếu một đơn vị kiến thức vẫn chưa đạt "
        "sau nhiều lần xử lý, đổi cách tiếp cận."
    ),
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
    [
        "Thứ 2",
        "Thứ 3",
        "Thứ 4",
        "Thứ 5",
        "Thứ 6",
        "Thứ 7",
        "Chủ nhật",
    ],
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

get_day_type_details = get_scheduler_symbol(
    scheduler,
    "get_day_type_details",
    lambda day_type_name: {
        "study_mode": "-",
        "start_time": "-",
        "duration": "-",
    },
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


if "month_selector" not in st.session_state:
    st.session_state.month_selector = (
        st.session_state.view_month
    )


if "year_selector" not in st.session_state:
    st.session_state.year_selector = (
        st.session_state.view_year
    )


# ============================================================
# NAVIGATION HELPERS
# ============================================================

def _sync_month_selectors():
    """
    Đồng bộ selectbox tháng và năm với tháng lịch đang xem.

    Việc này ngăn selectbox ghi đè ngược lại view_month
    và view_year sau khi người dùng bấm các nút điều hướng.
    """

    st.session_state.month_selector = (
        st.session_state.view_month
    )

    st.session_state.year_selector = (
        st.session_state.view_year
    )


# ============================================================
# NAVIGATION CALLBACKS
# ============================================================

def previous_month():
    if st.session_state.view_month == 1:
        st.session_state.view_month = 12
        st.session_state.view_year -= 1

    else:
        st.session_state.view_month -= 1

    _sync_month_selectors()


def next_month():
    if st.session_state.view_month == 12:
        st.session_state.view_month = 1
        st.session_state.view_year += 1

    else:
        st.session_state.view_month += 1

    _sync_month_selectors()


def go_to_today():
    st.session_state.view_year = today.year
    st.session_state.view_month = today.month
    st.session_state.selected_date = today

    _sync_month_selectors()


def select_date(target_date):
    st.session_state.selected_date = target_date


def go_to_purple_week():
    first_purple_week_start = (
        START_DATE
        + timedelta(
            days=BLOCK_LENGTH * 4
        )
    )

    st.session_state.view_year = (
        first_purple_week_start.year
    )

    st.session_state.view_month = (
        first_purple_week_start.month
    )

    st.session_state.selected_date = (
        first_purple_week_start
    )

    _sync_month_selectors()


# ============================================================
# SCHEDULE CACHE
# ============================================================

@st.cache_data(show_spinner=False)
def get_schedule(end_date):
    return generate_schedule(end_date)


# ============================================================
# CSS
# ============================================================

inject_dashboard_css()


# ============================================================
# HEADER
# ============================================================

render_app_header()


# ============================================================
# TODAY DATA
# ============================================================

today_schedule = get_schedule(
    max(today, START_DATE)
)

today_events = today_schedule.get(
    today,
    [],
)

current_block_number = get_block_number(
    today
)


# ============================================================
# TODAY HERO
# ============================================================

render_today_hero(
    today,
    today_events,
    START_DATE,
    current_block_number,
    format_vietnamese_date,
)


# ============================================================
# SELECTED DATE DATA
# ============================================================

selected_date = (
    st.session_state.selected_date
)

selected_schedule = get_schedule(
    max(
        selected_date,
        START_DATE,
    )
)

selected_events = selected_schedule.get(
    selected_date,
    [],
)


# ============================================================
# QUICK STATS
# ============================================================

render_quick_stats(
    current_block_number,
    len(today_events),
    selected_date,
)


st.divider()


# ============================================================
# MONTH NAVIGATION
# ============================================================

render_month_toolbar(
    previous_month,
    next_month,
    go_to_today,
    go_to_purple_week,
)


# ============================================================
# CURRENT MONTH DATA
# ============================================================

year = st.session_state.view_year
month = st.session_state.view_month


last_day = calendar.monthrange(
    year,
    month,
)[1]


month_end = date(
    year,
    month,
    last_day,
)


schedule = get_schedule(
    max(
        month_end,
        today,
        START_DATE,
    )
)


# ============================================================
# PURPLE WEEK INFORMATION
# ============================================================

first_purple_date = (
    START_DATE
    + timedelta(
        days=BLOCK_LENGTH * 4
    )
)


if date(year, month, 1) < first_purple_date:
    st.caption(
        (
            "Tuần tím đầu tiên xuất hiện từ "
            f"{first_purple_date.strftime('%d/%m/%Y')}"
        )
    )


# ============================================================
# CALENDAR + SELECTED DAY DETAILS
# ============================================================

calendar_col, detail_col = st.columns(
    [1.5, 1.0],
    gap="large",
)


with calendar_col:
    render_calendar_grid(
        year,
        month,
        schedule,
        today,
        st.session_state.selected_date,
        select_date,
    )


with detail_col:
    render_selected_day_details(
        selected_date,
        selected_events,
        get_block_number(selected_date),
        format_vietnamese_date,
        get_day_type_details,
        ERROR_TYPES,
        REPAIR_STATUSES,
    )


# ============================================================
# LEARNING RULE SECTIONS
# ============================================================

render_learning_rule_sections(
    PREREQUISITE_RULES,
    PERSISTENT_GAP_RULE,
    PURPLE_REVIEW_INFO,
)