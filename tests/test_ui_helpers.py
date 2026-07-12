from ui import get_event_color_key, get_event_label


def test_get_event_label_uses_emoji_and_subject():
    event = {"emoji": "🔴", "subject": "Anh"}

    assert get_event_label(event) == "🔴 Anh"


def test_get_event_color_key_maps_known_emoji():
    assert get_event_color_key({"emoji": "🔴"}) == "red"
    assert get_event_color_key({"emoji": "🟠"}) == "orange"
    assert get_event_color_key({"emoji": "🟣"}) == "purple"
    assert get_event_color_key({"emoji": "❓"}) == "neutral"
