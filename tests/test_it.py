import io

import pytest

import amazon_linux_extras


def test_no_args(capsys, monkeypatch):
    with pytest.raises(SystemExit) as wrapped:
        monkeypatch.setattr('sys.stdin', io.StringIO(None))
        amazon_linux_extras.main()
    assert wrapped.value.code == 1
