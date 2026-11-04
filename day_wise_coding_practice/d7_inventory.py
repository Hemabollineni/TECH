import pytest


# Function to update product stock
def update_stock(inventory, product, quantity):

    # Check whether quantity is valid
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    # Check whether product exists
    if product not in inventory:
        raise ValueError("Product does not exist")

    # Update stock
    inventory[product] = inventory[product] + quantity

    return inventory


# Test 1: Successful stock update
def test_update_stock():
    inventory = {
        "Laptop": 10,
        "Mouse": 20,
        "Keyboard": 15
    }

    result = update_stock(inventory, "Mouse", 5)

    assert result["Mouse"] == 25


# Test 2: Invalid product
def test_invalid_product():
    inventory = {"Laptop": 10, "Mouse": 20}

    with pytest.raises(ValueError):
        update_stock(inventory, "Monitor", 5)


# Test 3: Zero quantity
def test_zero_quantity():
    inventory = {"Laptop": 10}

    with pytest.raises(ValueError):
        update_stock(inventory, "Laptop", 0)


# Test 4: Negative quantity
def test_negative_quantity():
    inventory = {"Laptop": 10}

    with pytest.raises(ValueError):
        update_stock(inventory, "Laptop", -5)
        

# Test 5: Verify exact updated stock
def test_exact_stock_value():
    inventory = {"Laptop": 10}

    result = update_stock(inventory, "Laptop", 5)

    assert result == {"Laptop": 15}


# Test 6: Verify other products remain unchanged
def test_other_products_unchanged():
    inventory = {
        "Laptop": 10,
        "Mouse": 20,
        "Keyboard": 15
    }

    result = update_stock(inventory, "Mouse", 5)

    assert result["Laptop"] == 10
    assert result["Mouse"] == 25
    assert result["Keyboard"] == 15        
