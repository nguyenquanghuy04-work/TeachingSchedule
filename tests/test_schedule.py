from datetime import date, timedelta

from scheduler import START_DATE, generate_schedule, get_block_number


def labels_for_date(schedule, target_date):
    return [f"{event['emoji']}{event['subject']}" for event in schedule.get(target_date, [])]


def test_block_1():
    schedule = generate_schedule(date(2026, 7, 26))

    assert labels_for_date(schedule, date(2026, 7, 13)) == ["🔴Anh"]
    assert labels_for_date(schedule, date(2026, 7, 14)) == ["🟠Anh"]
    assert labels_for_date(schedule, date(2026, 7, 15)) == ["🔴Toán"]
    assert labels_for_date(schedule, date(2026, 7, 16)) == ["🟡Anh", "🟠Toán"]
    assert labels_for_date(schedule, date(2026, 7, 17)) == ["🔴Lý"]
    assert labels_for_date(schedule, date(2026, 7, 18)) == ["🟡Toán", "🟠Lý"]
    assert labels_for_date(schedule, date(2026, 7, 19)) == []
    assert labels_for_date(schedule, date(2026, 7, 20)) == ["🟢Anh", "🟡Lý"]
    assert labels_for_date(schedule, date(2026, 7, 21)) == []
    assert labels_for_date(schedule, date(2026, 7, 22)) == ["🟢Toán"]
    assert labels_for_date(schedule, date(2026, 7, 23)) == []
    assert labels_for_date(schedule, date(2026, 7, 24)) == ["🟢Lý"]
    assert labels_for_date(schedule, date(2026, 7, 25)) == ["🔵Anh", "🔵Toán"]
    assert labels_for_date(schedule, date(2026, 7, 26)) == ["🔵Lý", "⚫Vá lỗi"]


def test_block_2():
    schedule = generate_schedule(date(2026, 7, 31))

    assert labels_for_date(schedule, date(2026, 7, 27)) == ["🔴Anh"]
    assert labels_for_date(schedule, date(2026, 7, 28)) == ["🟠Anh"]
    assert labels_for_date(schedule, date(2026, 7, 29)) == ["🔴Toán"]
    assert labels_for_date(schedule, date(2026, 7, 30)) == ["🟡Anh", "🟠Toán"]
    assert labels_for_date(schedule, date(2026, 7, 31)) == ["🔴Lý"]


def test_future_schedule_and_boundaries():
    schedule = generate_schedule(date(2027, 12, 31))

    assert get_block_number(date(2027, 12, 31)) == ((date(2027, 12, 31) - START_DATE).days // 14) + 1
    assert get_block_number(START_DATE + timedelta(days=14)) == 2
    assert get_block_number(START_DATE + timedelta(days=28)) == 3
    assert all(event_date >= START_DATE for event_date in schedule) is True
    assert all(event_date >= START_DATE for event_date in schedule.keys()) is True
