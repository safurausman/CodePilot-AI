from io import StringIO
from unittest import TestCase, main
from unittest.mock import patch

import codepilot_generated_generate_code_optimize_code as calc


class TestCalculator(TestCase):
    """Test suite for the command-line calculator application."""

    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "10",
            "5",
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_addition(self, mock_stdout: StringIO, mock_input) -> None:
        """Test addition operation (option 1) followed by exit (option 5)."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Result: 10.0 + 5.0 = 15.0", output)
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "2",
            "10",
            "4",
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_subtraction(self, mock_stdout: StringIO, mock_input) -> None:
        """Test subtraction operation (option 2) followed by exit (option 5)."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Result: 10.0 - 4.0 = 6.0", output)
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "3",
            "6",
            "7",
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_multiplication(self, mock_stdout: StringIO, mock_input) -> None:
        """Test multiplication operation (option 3) followed by exit (option 5)."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Result: 6.0 * 7.0 = 42.0", output)
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "4",
            "10",
            "0",
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_division_by_zero(self, mock_stdout: StringIO, mock_input) -> None:
        """Test division by zero error handling (option 4) followed by exit."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Error: Division by zero is not allowed.", output)
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch("builtins.input", side_effect=["5"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_exit(self, mock_stdout: StringIO, mock_input) -> None:
        """Test immediate exit via option 5."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "1",
            "2",
            "3",  # First calculation: 2 + 3 = 5
            "4",
            "8",
            "2",  # Second calculation: 8 / 2 = 4.0
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_multiple_calculations(
        self, mock_stdout: StringIO, mock_input
    ) -> None:
        """Test performing multiple consecutive calculations before exiting."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn("Result: 2.0 + 3.0 = 5.0", output)
        self.assertIn("Result: 8.0 / 2.0 = 4.0", output)
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "6",
            "5",
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_menu_choice(
        self, mock_stdout: StringIO, mock_input
    ) -> None:
        """Test selecting an invalid menu option followed by exit."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn(
            "Invalid choice. Please select a valid option from 1 to 5.", output
        )
        self.assertIn("Exiting calculator. Goodbye!", output)

    @patch(
        "builtins.input",
        side_effect=[
            "1",   # Select addition
            "abc", # Invalid first number
            "5",   # Valid first number
            "5",   # Valid second number
            "5",   # Exit the calculator
        ],
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_invalid_numeric_input(
        self, mock_stdout: StringIO, mock_input
    ) -> None:
        """Test providing non-numeric input when asked for a number, then exiting."""
        calc.main()
        output = mock_stdout.getvalue()
        self.assertIn(
            "Invalid input. Please enter a valid number.", output
        )
        self.assertIn("Exiting calculator. Goodbye!", output)


if __name__ == "__main__":
    main()