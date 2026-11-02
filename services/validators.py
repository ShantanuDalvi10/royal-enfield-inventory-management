def validate_price_and_stock(price=None,stock=None):
    validated_price = None
    validated_stock = None

    if price is not None:
        try:
            validated_price = float(price)
        except (ValueError,TypeError):
            raise ValueError("Please enter a valid price")

        if validated_price < 0:
            raise ValueError("Price cannot be negative")

    if stock is not None:
        try:
            validated_stock = int(stock)
        except (ValueError,TypeError):
            raise ValueError("Enter valid stock")

        if validated_stock < 0:
            raise ValueError("Stock cannot be negative")

    return validated_price,validated_stock