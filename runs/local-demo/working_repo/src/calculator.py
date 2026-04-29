def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("division by zero is not allowed")
    return a / b
