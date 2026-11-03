import pytest


# Function to perform calculations
def calculate(a, b, operation):

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    else:
        raise ValueError("Invalid operation")


# Test 1: Addition
def test_add():
    assert calculate(10, 20, "add") == 30


# Test 2: Subtraction
def test_subtract():
    assert calculate(30, 10, "subtract") == 20


# Test 3: Multiplication
def test_multiply():
    assert calculate(5, 4, "multiply") == 20


# Test 4: Division
def test_divide():
    assert calculate(20, 5, "divide") == 4


# Test 5: Division by zero
def test_divide_by_zero():
    with pytest.raises(ValueError):
        calculate(20, 0, "divide")


# Test 6: Invalid operation
def test_invalid_operation():
    with pytest.raises(ValueError):
        calculate(10, 5, "modulus")