from datetime import date, datetime
from zoneinfo import ZoneInfo

from app import get_scheduler_symbol
from scheduler import (
    START_DATE,
    BLOCK_LENGTH,
    BLUE_TEST_INFO,
    ERROR_TYPES,
    REPAIR_STATUSES,
    generate_schedule,
    get_block_number,
    get_current_vietnam_date,
)


def event_labels(events):
    return [
        (event["emoji"], event["subject"])
        for event in events
    ]


def test_start_date():
    assert START_DATE == date(2026, 7, 13)


def test_block_length():
    assert BLOCK_LENGTH == 14


def test_no_events_before_start_date():
    schedule = generate_schedule(date(2026, 7, 12))
    assert schedule == {}


def test_july_2026_schedule():
    schedule = generate_schedule(date(2026, 7, 31))

    expected = {
        date(2026, 7, 13): [("🔴", "Anh")],
        date(2026, 7, 14): [("🟠", "Anh")],
        date(2026, 7, 15): [("🔴", "Toán")],
        date(2026, 7, 16): [
            ("🟡", "Anh"),
            ("🟠", "Toán"),
        ],
        date(2026, 7, 17): [("🔴", "Lý")],
        date(2026, 7, 18): [
            ("🟡", "Toán"),
            ("🟠", "Lý"),
        ],
        date(2026, 7, 19): [],
        date(2026, 7, 20): [
            ("🟢", "Anh"),
            ("🟡", "Lý"),
        ],
        date(2026, 7, 21): [],
        date(2026, 7, 22): [("🟢", "Toán")],
        date(2026, 7, 23): [],
        date(2026, 7, 24): [("🟢", "Lý")],
        date(2026, 7, 25): [
            ("🔵", "Anh"),
            ("🔵", "Toán"),
        ],
        date(2026, 7, 26): [
            ("🔵", "Lý"),
            ("⚫", "Vá lỗi"),
        ],
        date(2026, 7, 27): [("🔴", "Anh")],
        date(2026, 7, 28): [("🟠", "Anh")],
        date(2026, 7, 29): [("🔴", "Toán")],
        date(2026, 7, 30): [
            ("🟡", "Anh"),
            ("🟠", "Toán"),
        ],
        date(2026, 7, 31): [("🔴", "Lý")],
    }

    for target_date, expected_labels in expected.items():
        actual = event_labels(schedule.get(target_date, []))
        assert actual == expected_labels


def test_block_two_starts_on_july_27():
    assert get_block_number(date(2026, 7, 26)) == 1
    assert get_block_number(date(2026, 7, 27)) == 2


def test_future_schedule_december_2027():
    schedule = generate_schedule(date(2027, 12, 31))

    december_events = [
        event
        for event_date, events in schedule.items()
        if event_date.year == 2027
        and event_date.month == 12
        for event in events
    ]

    assert len(december_events) > 0


def test_schedule_crosses_year_boundary():
    schedule = generate_schedule(date(2027, 1, 31))

    assert any(
        event_date.year == 2027
        for event_date in schedule
    )


def test_blue_day_is_diagnostic_not_pass_fail():
    combined_text = " ".join(
        [
            BLUE_TEST_INFO["check_method"],
            BLUE_TEST_INFO["goal"],
            *BLUE_TEST_INFO["notes"],
        ]
    ).lower()

    assert "chẩn đoán" in combined_text
    assert "điểm tổng" in combined_text
    assert "pass/fail" in combined_text


def test_error_types_are_complete():
    assert [item["code"] for item in ERROR_TYPES] == [
        "A",
        "B",
        "C",
        "D",
    ]

    assert [item["name"] for item in ERROR_TYPES] == [
        "Chưa hiểu",
        "Quên kiến thức",
        "Áp dụng sai",
        "Bất cẩn",
    ]


def test_single_careless_error_does_not_require_relearning():
    careless = next(
        item
        for item in ERROR_TYPES
        if item["code"] == "D"
    )

    action = careless["action"].lower()

    assert "chưa cần ôn lại nếu chỉ xảy ra một lần" in action
    assert "lặp lại nhiều lần" in action


def test_repair_statuses_are_complete():
    assert [item["name"] for item in REPAIR_STATUSES] == [
        "Đã vá",
        "Tạm ổn",
        "Chưa vá được",
    ]


def test_first_block_red_day_has_no_previous_block_debt():
    schedule = generate_schedule(date(2026, 7, 13))
    event = schedule[date(2026, 7, 13)][0]

    combined_tasks = " ".join(event["tasks"]).lower()

    assert "kiểm tra kiến thức nền nếu cần" in combined_tasks
    assert "block trước" not in combined_tasks


def test_get_scheduler_symbol_returns_default_when_missing():
    assert get_scheduler_symbol(object(), "missing_attr", "fallback") == "fallback"


def test_second_block_red_day_can_handle_previous_debt():
    schedule = generate_schedule(date(2026, 7, 27))
    event = schedule[date(2026, 7, 27)][0]

    combined_tasks = " ".join(event["tasks"]).lower()

    assert "block trước" in combined_tasks
    assert "tạm ổn" in combined_tasks
    assert "chưa vá được" in combined_tasks
