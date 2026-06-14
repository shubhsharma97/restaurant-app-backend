from app.main import read_root, health


def test_read_root():
    result = read_root()
    assert "message" in result


def test_health():
    result = health()
    assert result == {"status": "healthy"}
