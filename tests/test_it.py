import io
import json

import pytest
from ansible.module_utils.six import PY2, BytesIO

import amzn2extra


def _run_module(monkeypatch, param):
    param = {
        'ANSIBLE_MODULE_ARGS': param
    }
    monkeypatch.setattr('amzn2extra.COMMAND_PATH', './tests/cmd')
    if PY2:
        monkeypatch.setattr(
            'sys.stdin',
            BytesIO(json.dumps(param))
        )
    else:
        monkeypatch.setattr(
            'sys.stdin',
            io.TextIOWrapper(BytesIO(json.dumps(param).encode()))
        )
    with pytest.raises(SystemExit) as wrapped:
        amzn2extra.main()
    return wrapped.value


def test_no_args(capsys, monkeypatch):
    if PY2:
        monkeypatch.setattr('sys.stdin', BytesIO(None))
    else:
        monkeypatch.setattr('sys.stdin', io.TextIOWrapper(BytesIO(None)))
    with pytest.raises(SystemExit) as wrapped:
        amzn2extra.main()
    assert wrapped.value.code == 1


@pytest.mark.parametrize(
    'topic,state,expected_changed',
    [
        ('example1', 'present', True),
        ('example1', 'absent', False),
        ('example2', 'present', False),
        ('example2', 'absent', True),
    ]
)
def test_state_handle(monkeypatch, capsys, topic, state, expected_changed):
    monkeypatch.setattr('ansible.module_utils.basic._ANSIBLE_ARGS', None)
    sys_exit = _run_module(
        monkeypatch, {'name': topic, 'state': state})
    assert sys_exit.code == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out.split('\n')[-2])
    assert result['changed'] is expected_changed


@pytest.mark.parametrize(
    'topic,expected_changed',
    [
        ('example1', True),
        ('example2', False),
    ]
)
def test_state_handle_default(monkeypatch, capsys, topic, expected_changed):
    monkeypatch.setattr('ansible.module_utils.basic._ANSIBLE_ARGS', None)
    sys_exit = _run_module(
        monkeypatch, {'name': topic})
    assert sys_exit.code == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out.split('\n')[-2])
    assert result['changed'] is expected_changed
