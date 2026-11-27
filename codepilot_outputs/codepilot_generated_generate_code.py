def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Returns the difference between two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Returns the quotient of two numbers.

    Raises:
        ZeroDivisionError: If the divisor (b) is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return a / b


def get_number(prompt: str) -> float:
    """Prompts the user for a valid number with input validation."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main() -> None:
    """Main loop for the calculator application."""
    print("=== Python Calculator ===")
    print("Select operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")

    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "5":
            print("Exiting calculator. Goodbye!")
            break

        if choice not in operations:
            print("Invalid choice. Please select a valid option from 1 to 5.")
            continue

        symbol, func = operations[choice]

        num1 = get_number("Enter first number: ")
        num2 = get_number("Enter second number: ")

        try:
            result = func(num1, num2)
            print(f"Result: {num1} {symbol} {num2} = {result}")
        except ZeroDivisionError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()