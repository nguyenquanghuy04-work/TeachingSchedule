from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

# ============================================================
# CẤU HÌNH CỐT LÕI
# ============================================================

START_DATE = date(2026, 7, 13)
BLOCK_LENGTH = 14

SUBJECTS = [
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
]

# ============================================================
# CÁC MỐC HỌC TẬP
# ============================================================

STAGES = [
    {
        "offset": 0,
        "emoji": "🔴",
        "name": "Ngày đỏ",
        "milestone": "Ngày 0",
        "tasks": [
            "Kiểm tra nhanh kiến thức cũ hoặc nợ kiến thức nếu có.",
            "Ưu tiên kiến thức chưa xử lý hết trong ngày đen của block trước.",
            "Ưu tiên kiến thức đang ở trạng thái Tạm ổn hoặc Chưa vá được.",
            "Kiểm tra kiến thức cũ là tiền đề trực tiếp cho bài mới nếu cần.",
            "Dạy kiến thức mới theo đúng lộ trình.",
        ],
        "first_block_tasks": [
            "Kiểm tra kiến thức nền nếu cần.",
            "Dạy kiến thức mới theo đúng lộ trình.",
        ],
        "check_method": "Kiểm tra trực tiếp trong buổi học.",
        "goal": (
            "Xử lý có chọn lọc những kiến thức cũ cần thiết và tiếp tục "
            "dạy kiến thức mới đúng tiến độ."
        ),
        "notes": [
            "Nếu kiểm tra nhanh đạt, đóng lỗi.",
            "Nếu chưa đạt, giải thích hoặc ôn nhanh rồi kiểm tra lại bằng một bài tương tự.",
            "Không để phần kiểm tra bài cũ chiếm quá nhiều thời gian và làm gián đoạn tiến độ học mới, trừ trường hợp thiếu kiến thức tiên quyết bắt buộc.",
        ],
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
        "goal": (
            "Tạo lần tiếp xúc và tái hiện đầu tiên sau buổi học, "
            "không chép máy móc."
        ),
        "notes": [],
    },
    {
        "offset": 3,
        "emoji": "🟡",
        "name": "Ngày vàng",
        "milestone": "Ngày 3",
        "tasks": [
            "Đọc lại bài.",
            "Làm bài tập.",
            "Tự giải thích lại kiến thức bằng lời của mình.",
            "Quay video để kiểm tra.",
        ],
        "check_method": "Qua video.",
        "goal": (
            "Kiểm tra khả năng chủ động nhớ lại và tự diễn giải kiến thức, "
            "thay vì chỉ nhận ra kiến thức khi nhìn thấy."
        ),
        "notes": [],
    },
    {
        "offset": 7,
        "emoji": "🟢",
        "name": "Ngày xanh lá",
        "milestone": "Ngày 7",
        "tasks": [
            "Đọc lại nhanh kiến thức.",
            "Làm bài tập.",
            "Tham gia buổi chữa bài trực tiếp online.",
        ],
        "check_method": "Chữa trực tiếp online.",
        "goal": (
            "Phát hiện những chỗ còn hiểu sai, sửa lỗi trước bài kiểm tra "
            "cuối block và củng cố khả năng vận dụng."
        ),
        "notes": [
            "Ngày xanh lá không quyết định chính thức đạt hay chưa đạt.",
            "Đây vẫn là một mốc học và củng cố.",
        ],
    },
]

# ============================================================
# NGÀY XANH DƯƠNG
# ============================================================

BLUE_TEST_INFO = {
    "emoji": "🔵",
    "name": "Ngày xanh dương",
    "milestone": "Kiểm tra chẩn đoán cuối block",
    "tasks": [
        "Hoàn thành bài kiểm tra cuối block.",
        "Xác định chính xác L sai đơn vị kiến thức nào.",
        "Xác định nguyên nhân của từng lỗi sai.",
        "Phân loại lỗi thành: Chưa hiểu, Quên kiến thức, Áp dụng sai hoặc Bất cẩn.",
        "Xác định đơn vị kiến thức nào thực sự cần được đưa vào ngày đen để xử lý.",
    ],
    "check_method": (
        "Bài kiểm tra chẩn đoán theo từng đơn vị kiến thức; "
        "điểm tổng chỉ mang tính mô tả thứ cấp."
    ),
    "goal": (
        "Chẩn đoán chính xác từng đơn vị kiến thức L chưa nắm, còn hiểu sai "
        "hoặc cần củng cố; không dùng điểm tổng để tự động quyết định "
        "pass/fail toàn block hoặc học lại toàn bộ chương."
    ),
    "notes": [
        "Không reset toàn bộ chương chỉ vì điểm tổng thấp.",
        "Không có ngưỡng điểm tổng quan trọng để quyết định học lại toàn bộ chương.",
        "Mỗi câu hỏi nên được liên kết với một hoặc nhiều đơn vị kiến thức.",
        "Quyết định xử lý phải dựa trên kiến thức cụ thể bị sai, nguyên nhân sai, mức độ quan trọng và vai trò tiên quyết của kiến thức đó.",
    ],
}

# ============================================================
# PHÂN LOẠI LỖI SAU KIỂM TRA
# ============================================================

ERROR_TYPES = [
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
        "symptom": (
            "Biết kiến thức nhưng chọn sai phương pháp hoặc sai quy trình."
        ),
        "action": "Làm thêm bài tương tự.",
    },
    {
        "code": "D",
        "name": "Bất cẩn",
        "symptom": "Tính nhầm, sai dấu, đọc thiếu đề hoặc lỗi tương tự.",
        "action": (
            "Ghi nhận; chưa cần ôn lại nếu chỉ xảy ra một lần. "
            "Chỉ đưa vào danh sách cần xử lý nếu lặp lại nhiều lần "
            "và trở thành một xu hướng."
        ),
    },
]

# ============================================================
# NGÀY ĐEN
# ============================================================

BLACK_REPAIR_INFO = {
    "emoji": "⚫",
    "name": "Ngày đen",
    "milestone": "Vá lỗi tập trung",
    "tasks": [
        "Xác định chính xác đơn vị kiến thức cần xử lý.",
        "Giải thích lại ngắn gọn.",
        "Làm lại có hướng dẫn.",
        "Làm một bài tương tự độc lập.",
        "Đánh giá trạng thái sau khi xử lý.",
    ],
    "check_method": "Đánh giá lại riêng từng đơn vị kiến thức.",
    "goal": (
        "Ôn cấp tốc và sửa đúng những đơn vị kiến thức cần xử lý; "
        "không học lại toàn bộ chương nếu không cần thiết."
    ),
    "priority_order": [
        "Kiến thức tiên quyết cho block tiếp theo.",
        "Kiến thức chưa hiểu bản chất.",
        "Kiến thức bị quên.",
        "Kiến thức bị áp dụng sai.",
        "Lỗi bất cẩn lặp lại thành xu hướng.",
    ],
    "notes": [
        "Không reset toàn bộ chương.",
        "Chỉ xử lý đúng phần kiến thức bị hổng.",
        "Nếu không đủ thời gian, toàn bộ phần chưa xử lý được chuyển sang phần kiểm tra bài cũ của ngày đỏ block tiếp theo.",
    ],
}

# ============================================================
# TRẠNG THÁI SAU NGÀY ĐEN
# ============================================================

REPAIR_STATUSES = [
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
        "next_action": (
            "Bắt buộc đưa vào kiểm tra bài cũ ngày đỏ của block sau."
        ),
    },
]

# ============================================================
# QUY TẮC KIẾN THỨC TIÊN QUYẾT
# ============================================================

PREREQUISITE_RULES = {
    "not_required_for_next_block": (
        "Nếu kiến thức chưa đạt không liên quan trực tiếp đến block tiếp theo, "
        "tiếp tục học block mới bình thường và xử lý phần cũ song song."
    ),
    "required_for_next_block": (
        "Nếu kiến thức chưa đạt là điều kiện tiên quyết bắt buộc cho block tiếp theo, "
        "ưu tiên xử lý kiến thức đó ở đầu ngày đỏ trước khi dạy bài mới."
    ),
    "severe_gap": (
        "Chỉ khi lỗ hổng quá nghiêm trọng và khiến L không thể tiếp thu bài mới "
        "mới cân nhắc điều chỉnh nội dung block; không tự động reset toàn bộ chu kỳ."
    ),
}

# ============================================================
# LỖ HỔNG DAI DẲNG
# ============================================================

PERSISTENT_GAP_RULE = (
    "Nếu một đơn vị kiến thức vẫn chưa đạt sau nhiều lần xử lý, "
    "đánh dấu là lỗ hổng dai dẳng và thay đổi cách giải thích, dạng bài, "
    "ví dụ hoặc phương pháp tiếp cận thay vì tiếp tục lặp lại cùng một cách dạy."
)

# ============================================================
# NGÀY TÍM
# ============================================================

PURPLE_REVIEW_INFO = {
    "emoji": "🟣",
    "name": "Ngày tím",
    "milestone": "Tổng ôn định kỳ 2 tháng",
    "tasks": [
        "Hệ thống hóa các kiến thức đã học.",
        "Kiểm tra khả năng nhớ dài hạn.",
        "Kết nối kiến thức giữa các chương.",
        "Làm bài tập tổng hợp.",
        "Phát hiện kiến thức từng đạt nhưng sau thời gian dài đã bị quên.",
        "Xử lý các lỗ hổng dai dẳng còn tồn tại.",
    ],
    "priority": [
        "Kiến thức cốt lõi.",
        "Kiến thức từng sai.",
        "Kiến thức có tính liên kết cao.",
        "Kiến thức cần cho giai đoạn tiếp theo.",
    ],
    "note": (
        "Không dành quá nhiều thời gian cho những phần L đã thành thạo rõ ràng."
    ),
}

# ============================================================
# DATE HELPERS
# ============================================================

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


def get_current_vietnam_date():
    return datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).date()


def get_block_number(target_date):
    if target_date < START_DATE:
        return None

    days_since_start = (target_date - START_DATE).days
    return days_since_start // BLOCK_LENGTH + 1


def get_block_start(block_number):
    if block_number < 1:
        raise ValueError("block_number phải lớn hơn hoặc bằng 1.")

    return START_DATE + timedelta(
        days=(block_number - 1) * BLOCK_LENGTH
    )

# ============================================================
# EVENT FACTORIES
# ============================================================


def add_event(schedule, event_date, event):
    schedule.setdefault(event_date, []).append(event)


def get_day_type_details(day_type_name):
    details_map = {
        "Ngày đỏ": {
            "study_mode": "Online",
            "start_time": "19:45",
            "duration": "2 giờ 30 phút",
        },
        "Ngày cam": {
            "study_mode": "Tự học, chỉ kiểm tra kết quả qua ảnh",
            "start_time": "-",
            "duration": "-",
        },
        "Ngày vàng": {
            "study_mode": "Tự học, chỉ kiểm tra kết quả qua video",
            "start_time": "-",
            "duration": "-",
        },
        "Ngày xanh lá": {
            "study_mode": "Online",
            "start_time": "20:00",
            "duration": "1 giờ 30 phút",
        },
        "Ngày xanh dương": {
            "study_mode": "Làm bài kiểm tra",
            "start_time": "-",
            "duration": "1 giờ 30 phút",
        },
        "Ngày đen": {
            "study_mode": "Online/tùy tình hình thực tế",
            "start_time": "-",
            "duration": "-",
        },
        "Ngày tím": {
            "study_mode": "Online",
            "start_time": "19:45",
            "duration": "2 giờ 30 phút",
        },
    }

    return details_map.get(day_type_name, {
        "study_mode": "-",
        "start_time": "-",
        "duration": "-",
    })


def create_study_event(subject, stage, block_number):
    tasks = (
        stage.get("first_block_tasks", stage["tasks"])
        if block_number == 1
        else stage["tasks"]
    )

    details = get_day_type_details(stage["name"])

    return {
        "type": "study",
        "emoji": stage.get("emoji", ""),
        "subject": subject["short"],
        "full_subject": subject["name"],
        "stage": stage["name"],
        "milestone": stage.get("milestone", ""),
        "tasks": tasks,
        "check_method": stage["check_method"],
        "goal": stage["goal"],
        "notes": stage.get("notes", []),
        "block": block_number,
        "study_mode": details["study_mode"],
        "start_time": details["start_time"],
        "duration": details["duration"],
    }


def create_test_event(subject, block_number):
    details = get_day_type_details(BLUE_TEST_INFO["name"])

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
        "notes": BLUE_TEST_INFO["notes"],
        "block": block_number,
        "study_mode": details["study_mode"],
        "start_time": details["start_time"],
        "duration": details["duration"],
    }


def create_repair_event(block_number):
    details = get_day_type_details(BLACK_REPAIR_INFO["name"])

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
        "notes": BLACK_REPAIR_INFO["notes"],
        "priority_order": BLACK_REPAIR_INFO["priority_order"],
        "block": block_number,
        "study_mode": details["study_mode"],
        "start_time": details["start_time"],
        "duration": details["duration"],
    }

# ============================================================
# SCHEDULE GENERATION
# ============================================================


def generate_schedule(end_date):
    """
    Sinh lịch từ START_DATE đến end_date.

    Sau mỗi 4 block, chèn một tuần tổng ôn màu tím với 3 ngày:
    Thứ Hai, Thứ Tư, Thứ Sáu của tuần đó.
    """

    schedule = {}

    if end_date < START_DATE:
        return schedule

    block_number = 1
    block_start = START_DATE

    while block_start <= end_date:
        if block_number > 1 and (block_number - 1) % 4 == 0:
            purple_week_start = block_start

            purple_dates = [
                purple_week_start + timedelta(days=0),
                purple_week_start + timedelta(days=2),
                purple_week_start + timedelta(days=4),
            ]

            for index, purple_date in enumerate(purple_dates):
                if purple_date <= end_date:
                    subject = SUBJECTS[index]
                    event = create_study_event(
                        subject,
                        {
                            "name": "Ngày tím",
                            "emoji": "🟣",
                            "milestone": PURPLE_REVIEW_INFO["milestone"],
                            "tasks": PURPLE_REVIEW_INFO["tasks"],
                            "check_method": "Tự đánh giá năng lực tổng hợp.",
                            "goal": "Tổng ôn và củng cố kiến thức dài hạn.",
                            "notes": [PURPLE_REVIEW_INFO["note"]],
                        },
                        block_number,
                    )
                    add_event(schedule, purple_date, event)

            block_start += timedelta(days=7)

        # Chu kỳ Ngày 0 → Ngày 1 → Ngày 3 → Ngày 7
        for subject in SUBJECTS:
            red_day = block_start + timedelta(days=subject["offset"])

            for stage in STAGES:
                event_date = red_day + timedelta(days=stage["offset"])

                if event_date <= end_date:
                    add_event(
                        schedule,
                        event_date,
                        create_study_event(
                            subject,
                            stage,
                            block_number,
                        ),
                    )

        # Thứ Bảy tuần 2: kiểm tra hai môn đầu tiên
        saturday_week_2 = block_start + timedelta(days=12)

        if saturday_week_2 <= end_date:
            for subject in SUBJECTS[:2]:
                add_event(
                    schedule,
                    saturday_week_2,
                    create_test_event(subject, block_number),
                )

        # Chủ nhật tuần 2: kiểm tra môn còn lại + ngày đen
        sunday_week_2 = block_start + timedelta(days=13)

        if sunday_week_2 <= end_date:
            add_event(
                schedule,
                sunday_week_2,
                create_test_event(
                    SUBJECTS[2],
                    block_number,
                ),
            )

            add_event(
                schedule,
                sunday_week_2,
                create_repair_event(block_number),
            )

        block_start += timedelta(days=BLOCK_LENGTH)
        block_number += 1

    return schedule
