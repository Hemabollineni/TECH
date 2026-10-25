import pytest


@pytest.fixture
def numbers():
    return [10, 20, 30]


def test_first_number(numbers):
    assert numbers[0] == 10


def test_list_length(numbers):
    assert len(numbers) == 3