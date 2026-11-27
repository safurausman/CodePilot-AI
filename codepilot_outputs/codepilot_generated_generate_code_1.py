"""
A robust, menu-driven command-line calculator in Python.
Supports basic arithmetic operations: addition, subtraction, 
multiplication, and division with input validation and error handling.
"""

def add(number_one: float, number_two: float) -> float:
    """Returns the sum of two numbers."""
    return number_one + number_two


def subtract(number_one: float, number_two: float) -> float:
    """Returns the difference between two numbers."""
    return number_one - number_two


def multiply(number_one: float, number_two: float) -> float:
    """Returns the product of two numbers."""
    return number_one * number_two


def divide(number_one: float, number_two: float) -> float:
    """
    Returns the quotient of two numbers.
    Raises ZeroDivisionError if the second number is zero.
    """
    if number_two == 0:
        raise ZeroDivisionError("Division by zero is not allowed.")
    return number_one / number_two


def get_numeric_input(prompt: str) -> float:
    """
    Prompts the user until a valid floating-point number is entered.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def display_menu() -> None:
    """Displays the main calculator menu to the user."""
    print("\n--- Python Calculator ---")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    print("5. Exit")


def main() -> None:
    """Main function to control the calculator workflow and loop."""
    operations = {
        '1': ("Addition", add),
        '2': ("Subtraction", subtract),
        '3': ("Multiplication", multiply),
        '4': ("Division", divide)
    }

    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break

        if choice in operations:
            operation_name, operation_func = operations[choice]
            print(f"\n--- {operation_name} ---")
            
            num1 = get_numeric_input("Enter the first number: ")
            num2 = get_numeric_input("Enter the second number: ")

            try:
                result = operation_func(num1, num2)
                print(f"Result: {num1} and {num2} = {result}")
            except ZeroDivisionError as error:
                print(f"Error: {error}")
        else:
            print("Invalid choice. Please select a valid option from the menu (1-5).")


if __name__ == "__main__":
    main()