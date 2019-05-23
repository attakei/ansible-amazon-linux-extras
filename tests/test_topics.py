import pytest

from amazon_linux_extras import Topic


@pytest.mark.parametrize(
    'line,expected_name,expected_version,expected_status',
    [
        (
            '  0  ansible2                 available    [ =2.4.2  =2.4.6 ]',
            'ansible2',
            None,
            'available',
        ),
        (
            '  2  httpd_modules            available    [ =1.0 ]',
            'httpd_modules',
            None,
            'available',
        ),
        (
            '  2  httpd_modules=latest            enabled    [ =1.0 ]',
            'httpd_modules',
            'latest',
            'enabled',
        ),
        (
            '  2  httpd_modules=1.0            enabled    [ =1.0 ]',
            'httpd_modules',
            '1.0',
            'enabled',
        ),
    ]
)
def test_convert_single_line(
        line, expected_name, expected_version, expected_status):
    topic = Topic.from_text(line)
    assert topic.name == expected_name
    assert topic.version == expected_version
    assert topic.status == expected_status
