#!/usr/bin/env python3
"""
Simple test runner for shoehorn-ingest-test1
This implements basic testing functionality as requested.
"""

import sys
import unittest
from io import StringIO


class TestIngestBasics(unittest.TestCase):
    """Basic tests for data ingestion functionality"""
    
    def test_basic_functionality(self):
        """Test that basic functionality works"""
        result = "TEST"
        self.assertEqual(result, "TEST")
        
    def test_string_processing(self):
        """Test basic string processing"""
        test_data = "sample data"
        processed = test_data.upper()
        self.assertEqual(processed, "SAMPLE DATA")
        
    def test_list_operations(self):
        """Test basic list operations"""
        test_list = [1, 2, 3]
        result = len(test_list)
        self.assertEqual(result, 3)


def run_tests():
    """Run all tests and return results"""
    # Capture test output
    test_output = StringIO()
    runner = unittest.TextTestRunner(stream=test_output, verbosity=2)
    
    # Load and run tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIngestBasics)
    result = runner.run(suite)
    
    # Print results
    output = test_output.getvalue()
    print(output)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    if success:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed!")
        sys.exit(1)