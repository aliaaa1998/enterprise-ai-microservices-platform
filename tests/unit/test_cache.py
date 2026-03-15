from shared.core.cache import make_cache_key


def test_make_cache_key_stable() -> None:
    key1 = make_cache_key("summarize", "abc")
    key2 = make_cache_key("summarize", "abc")
    assert key1 == key2
