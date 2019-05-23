import io
import json

import pytest

import amazon_linux_extras


def _run_module(monkeypatch, param):
    param = {
        'ANSIBLE_MODULE_ARGS': param
    }
    with pytest.raises(SystemExit) as wrapped:
        monkeypatch.setattr('sys.stdin', io.BytesIO(json.dumps(param)))
        amazon_linux_extras.main()
    return wrapped.value


def test_no_args(capsys, monkeypatch):
    with pytest.raises(SystemExit) as wrapped:
        monkeypatch.setattr('sys.stdin', io.StringIO(None))
        amazon_linux_extras.main()
    assert wrapped.value.code == 1


def test_absent_to_absent(capsys, monkeypatch):
    monkeypatch.setattr('ansible.module_utils.basic._ANSIBLE_ARGS', None)
    sys_exit = _run_module(monkeypatch, {'name': 'example'})
    assert sys_exit.code == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out.split('\n')[-2])
    assert result['changed'] is False
