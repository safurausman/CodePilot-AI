import unittest
from modules.tools.safe_python import execute_safe_python

class SafePythonToolTests(unittest.TestCase):
    def test_math_expression(self):
        self.assertEqual(execute_safe_python("sum([1, 2, 3])"), "6")
    def test_safe_math_function(self):
        self.assertEqual(execute_safe_python("sqrt(81)"), "9.0")
    def test_rejects_imports(self):
        with self.assertRaises(ValueError):
            execute_safe_python("__import__('os').system('echo unsafe')")
    def test_rejects_attribute_access(self):
        with self.assertRaises(ValueError):
            execute_safe_python("(1).__class__")

if __name__ == "__main__":
    unittest.main()
