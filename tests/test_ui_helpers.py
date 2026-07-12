from ui import build_day_button_label, get_event_color_key, get_event_label, get_short_subject


def test_get_event_label_uses_emoji_and_subject():
    event = {"emoji": "🔴", "subject": "Anh"}

    assert get_event_label(event) == "🔴 Anh"


def test_get_event_color_key_maps_known_emoji():
    assert get_event_color_key({"emoji": "🔴"}) == "red"
    assert get_event_color_key({"emoji": "🟠"}) == "orange"
    assert get_event_color_key({"emoji": "🟣"}) == "purple"
    assert get_event_color_key({"emoji": "❓"}) == "neutral"


def test_get_short_subject_maps_known_subjects():
    assert get_short_subject("Tiếng Anh") == "Anh"
    assert get_short_subject("Toán") == "Toán"
    assert get_short_subject("Vật lý") == "Lý"


def test_build_day_button_label_uses_plain_text_lines():
    label = build_day_button_label(16, [{"emoji": "🟡", "subject": "Tiếng Anh"}, {"emoji": "🟠", "subject": "Toán"}], is_today=True)

    assert "✓ • 16" in label
    assert "🟡 Anh" in label
    assert "🟠 Toán" in label
    assert "<div" not in label
    assert "</div>" not in label
