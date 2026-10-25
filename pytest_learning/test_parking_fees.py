import pytest
from parking_fees import calculate_fee

def test_two_wheeler_for_two_hours():
    assert calculate_fee(2, "2-wheeler") == 40


def test_four_wheeler_for_three_hours():
    assert calculate_fee(3, "4-wheeler") == 90


def test_zero_hours_raises_value_error():
    with pytest.raises(ValueError):
        calculate_fee(0, "2-wheeler")


def test_invalid_vehicle_type_raises_value_error():
    with pytest.raises(ValueError):
        calculate_fee(2, "3-wheeler")

# def test_calculate_parking_fee():
#     # Test for 2-wheeler
#     assert calculate_parking_fee(2, "2-wheeler") == 40
#     assert calculate_parking_fee(5, "2-wheeler") == 100

#     # Test for 4-wheeler
#     assert calculate_parking_fee(3, "4-wheeler") == 90
#     assert calculate_parking_fee(6, "4-wheeler") == 180

#     # Test for invalid vehicle type
#     try:
#         calculate_parking_fee(2, "3-wheeler")
#     except ValueError as e:
#         assert str(e) == "Invalid vehicle type. Must be '2-wheeler' or '4-wheeler'."

#     # Test for invalid hours
#     try:
#         calculate_parking_fee(-1, "2-wheeler")
#     except ValueError as e:
#         assert str(e) == "Hours must be greater than zero."
        