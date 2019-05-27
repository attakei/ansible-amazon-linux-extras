import io
import json

import pytest

import amzn2extra


def _run_module(monkeypatch, param):
    param = {
        'ANSIBLE_MODULE_ARGS': param
    }
    monkeypatch.setattr('amzn2extra.COMMAND_PATH', './tests/cmd')
    with pytest.raises(SystemExit) as wrapped:
        monkeypatch.setattr('sys.stdin', io.BytesIO(json.dumps(param)))
        amzn2extra.main()
    return wrapped.value


def test_no_args(capsys, monkeypatch):
    with pytest.raises(SystemExit) as wrapped:
        monkeypatch.setattr('sys.stdin', io.StringIO(None))
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
