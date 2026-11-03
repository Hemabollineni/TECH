
def calculate_item_total(price, quantity):
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise ValueError("Price must be a number")

    if price <= 0:
        raise ValueError("Price must be greater than zero")

    if not isinstance(quantity, int) or isinstance(quantity, bool):
        raise ValueError("Quantity must be a whole number")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    return price * quantity


def calculate_checkout_total(items):
    if not isinstance(items, list):
        raise ValueError("Items must be a list")

    if not items:
        raise ValueError("Cart cannot be empty")

    total = 0

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each item must be a dictionary")

        if "price" not in item or "quantity" not in item:
            raise ValueError("Each item needs price and quantity")

        total += calculate_item_total(
            item["price"],
            item["quantity"]
        )

    return total

