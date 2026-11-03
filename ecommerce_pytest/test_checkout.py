
import pytest

from checkout import (
    calculate_item_total,
    calculate_checkout_total,
)


def test_single_product_total():
    result = calculate_item_total(500, 2)

    assert result == 1000


def test_checkout_with_multiple_products(cart_data):
    result = calculate_checkout_total(cart_data)
    assert result == 2200


def test_reject_zero_price():
    with pytest.raises(ValueError):
        calculate_item_total(0, 2)


def test_reject_zero_quantity():
    with pytest.raises(ValueError):
        calculate_item_total(500, 0)


def test_reject_empty_cart():
    with pytest.raises(ValueError):
        calculate_checkout_total([])


@pytest.mark.parametrize(
    "price, quantity, expected",
    [
        (100, 1, 100),
        (250, 4, 1000),
        (800, 3, 2400),
        (50, 10, 500),
    ],
)
def test_item_total_with_multiple_inputs(price, quantity, expected):
    result = calculate_item_total(price, quantity)

    assert result == expected


@pytest.mark.parametrize(
    "quantity",
    [0, -2, 1.5],
)
def test_reject_invalid_quantities(quantity):

    with pytest.raises(ValueError):
        calculate_item_total(100, quantity)

@pytest.mark.parametrize(
    "price",
    [0, -100, "500"],
)
def test_reject_invalid_prices(price):
    with pytest.raises(ValueError):
        calculate_item_total(price, 2)
        
@pytest.mark.parametrize(
    "price",
    [0, -100, "500"],
)
def test_reject_invalid_prices(price):
    with pytest.raises(ValueError):
        calculate_item_total(price, 2)        
        
# Test missing product information
def test_reject_product_with_missing_quantity():
    items = [
        {"price": 500}
    ]

    with pytest.raises(ValueError):
        calculate_checkout_total(items)
        
# Test invalid cart item        
def test_reject_invalid_cart_item():
    items = ["Laptop"]

    with pytest.raises(ValueError):
        calculate_checkout_total(items)


@pytest.fixture
def cart_data():
    return [
        {"price": 500, "quantity": 2},
        {"price": 1200, "quantity": 1},
    ]

@pytest.fixture(scope="module")
def discount_rate():
    print("\nCreating discount rate")
    return 10

def test_discount_for_laptop(discount_rate):
    price = 1000
    discount = price * discount_rate / 100
    assert discount == 100


def test_discount_for_mobile(discount_rate):
    price = 2000
    discount = price * discount_rate / 100
    assert discount == 200


def test_discount_for_keyboard(discount_rate):
    price = 500
    discount = price * discount_rate / 100
    assert discount == 50