import pytest

from consumer import last_full_minute


@pytest.mark.parametrize('timestamp, expected', [
    (1660401937567, 1660401900000),  # Saturday, 13 August 2022 14:45:37.567 -> 14:45:00.000
    (1660401984126, 1660401960000)  # Saturday, 13 August 2022 14:46:24.126 -> 14:46:00.000
])
def test_last_full_minute__valid_input__returns_correct_result(timestamp, expected):
    # given
    # timestamp

    # when
    actual = last_full_minute(timestamp)

    # then
    assert actual == expected

