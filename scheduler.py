import calendar
from datetime import date, timedelta

START_DATE = date(2026, 7, 13)
BLOCK_LENGTH = 14

SUBJECTS = [
    {"name": "Tiếng Anh", "short": "Anh", "offset": 0},
    {"name": "Toán", "short": "Toán", "offset": 2},
    {"name": "Vật lý", "short": "Lý", "offset": 4},
]

STAGES = [
    {
        "offset": 0,
        "emoji": "🔴",
        "name": "Ngày đỏ",
        "milestone": "Ngày 0",
        "tasks": [
            "Kiểm tra nhanh kiến thức cũ hoặc nợ kiến thức nếu có.",
            "Ưu tiên kiến thức chưa xử lý hết từ block trước.",
            "Dạy kiến thức mới theo đúng lộ trình.",
        ],
        "check_method": "Kiểm tra trực tiếp trong buổi học.",
        "goal": "Kiểm tra kiến thức cũ cần thiết và bắt đầu chu kỳ học kiến thức mới.",
    },
    {
        "offset": 1,
        "emoji": "🟠",
        "name": "Ngày cam",
        "milestone": "Ngày 1",
        "tasks": [
            "Cố gắng tự nhớ kiến thức trước khi xem lại tài liệu.",
            "Chép lại kiến thức đã học một lần.",
            "Gửi ảnh để kiểm tra việc hoàn thành.",
        ],
        "check_method": "Qua ảnh.",
        "goal": "Tạo lần tái hiện kiến thức đầu tiên sau buổi học.",
    },
    {
        "offset": 3,
        "emoji": "🟡",
        "name": "Ngày vàng",
        "milestone": "Ngày 3",
        "tasks": [
            "Đọc lại bài.",
            "Làm bài tập.",
            "Tự giải thích kiến thức bằng lời của mình.",
            "Quay video để kiểm tra.",
        ],
        "check_method": "Qua video.",
        "goal": "Kiểm tra khả năng chủ động nhớ lại và tự diễn giải kiến thức.",
    },
    {
        "offset": 7,
        "emoji": "🟢",
        "name": "Ngày xanh lá",
        "milestone": "Ngày 7",
        "tasks": [
            "Đọc lại nhanh kiến thức.",
            "Làm bài tập.",
            "Tham gia chữa bài trực tiếp online.",
        ],
        "check_method": "Chữa trực tiếp online.",
        "goal": "Phát hiện chỗ còn hiểu sai, sửa lỗi và củng cố khả năng vận dụng trước bài kiểm tra cuối block.",
    },
]

BLUE_TEST_INFO = {
    "emoji": "🔵",
    "name": "Ngày xanh dương",
    "milestone": "Kiểm tra cuối block",
    "tasks": [
        "Hoàn thành bài kiểm tra cuối block.",
        "Mỗi câu sai cần được liên kết với đơn vị kiến thức tương ứng.",
        "Xác định nguyên nhân sai: chưa hiểu, quên, áp dụng sai hoặc bất cẩn.",
    ],
    "check_method": "Bài kiểm tra đánh giá cuối block.",
    "goal": "Đánh giá chính thức mức độ nắm vững từng đơn vị kiến thức, không chỉ dựa vào điểm tổng.",
}

BLACK_REPAIR_INFO = {
    "emoji": "⚫",
    "name": "Ngày đen",
    "milestone": "Vá lỗi cuối block",
    "tasks": [
        "Xác định chính xác đơn vị kiến thức chưa đạt.",
        "Giải thích lại ngắn gọn.",
        "Làm lại có hướng dẫn.",
        "Làm một bài tương tự độc lập.",
        "Đánh giá trạng thái: Đã vá, Tạm ổn hoặc Chưa vá được.",
    ],
    "check_method": "Đánh giá lại theo từng đơn vị kiến thức.",
    "goal": "Chỉ sửa đúng phần còn yếu, không học lại toàn bộ chương. Phần chưa xử lý hết được chuyển sang ngày đỏ của block tiếp theo.",
}

WEEKDAY_NAMES = [
    "Thứ Hai",
    "Thứ Ba",
    "Thứ Tư",
    "Thứ Năm",
    "Thứ Sáu",
    "Thứ Bảy",
    "Chủ nhật",
]

CALENDAR_HEADERS = [
    "Thứ 2",
    "Thứ 3",
    "Thứ 4",
    "Thứ 5",
    "Thứ 6",
    "Thứ 7",
    "Chủ nhật",
]


def format_vietnamese_date(value):
    weekday = WEEKDAY_NAMES[value.weekday()]
    return f"{weekday}, {value.strftime('%d/%m/%Y')}"


def get_block_number(target_date):
    if target_date < START_DATE:
        return None
    days_since_start = (target_date - START_DATE).days
    return days_since_start // BLOCK_LENGTH + 1


def add_event(schedule, event_date, event):
    schedule.setdefault(event_date, []).append(event)


def create_study_event(subject, stage, block_number):
    return {
        "type": "study",
        "emoji": stage["emoji"],
        "subject": subject["short"],
        "full_subject": subject["name"],
        "stage": stage["name"],
        "milestone": stage["milestone"],
        "tasks": stage["tasks"],
        "check_method": stage["check_method"],
        "goal": stage["goal"],
        "block": block_number,
    }


def create_test_event(subject, block_number):
    return {
        "type": "test",
        "emoji": BLUE_TEST_INFO["emoji"],
        "subject": subject["short"],
        "full_subject": subject["name"],
        "stage": BLUE_TEST_INFO["name"],
        "milestone": BLUE_TEST_INFO["milestone"],
        "tasks": BLUE_TEST_INFO["tasks"],
        "check_method": BLUE_TEST_INFO["check_method"],
        "goal": BLUE_TEST_INFO["goal"],
        "block": block_number,
    }


def create_repair_event(block_number):
    return {
        "type": "repair",
        "emoji": BLACK_REPAIR_INFO["emoji"],
        "subject": "Vá lỗi",
        "full_subject": "Cả 3 môn",
        "stage": BLACK_REPAIR_INFO["name"],
        "milestone": BLACK_REPAIR_INFO["milestone"],
        "tasks": BLACK_REPAIR_INFO["tasks"],
        "check_method": BLACK_REPAIR_INFO["check_method"],
        "goal": BLACK_REPAIR_INFO["goal"],
        "block": block_number,
    }


def generate_schedule(end_date):
    schedule = {}

    if end_date < START_DATE:
        return schedule

    block_number = 1
    block_start = START_DATE

    while block_start <= end_date:
        for subject in SUBJECTS:
            red_day = block_start + timedelta(days=subject["offset"])
            for stage in STAGES:
                event_date = red_day + timedelta(days=stage["offset"])
                if event_date <= end_date:
                    add_event(schedule, event_date, create_study_event(subject, stage, block_number))

        saturday_week_2 = block_start + timedelta(days=12)
        if saturday_week_2 <= end_date:
            for subject in SUBJECTS[:2]:
                add_event(schedule, saturday_week_2, create_test_event(subject, block_number))

        sunday_week_2 = block_start + timedelta(days=13)
        if sunday_week_2 <= end_date:
            add_event(schedule, sunday_week_2, create_test_event(SUBJECTS[2], block_number))
            add_event(schedule, sunday_week_2, create_repair_event(block_number))

        block_start += timedelta(days=BLOCK_LENGTH)
        block_number += 1

    return schedule
