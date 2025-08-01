import unittest
from src.counter import Counter

class TestCounter(unittest.TestCase):

    def setUp(self):
        self.counter = Counter()

    def test_initial_count(self):
        self.assertEqual(self.counter.get_count(), 0)

    def test_start_counting(self):
        self.counter.start_counting()
        self.assertTrue(self.counter.is_counting)

    def test_stop_counting(self):
        self.counter.start_counting()
        self.counter.stop_counting()
        self.assertFalse(self.counter.is_counting)

    def test_count_increment(self):
        self.counter.start_counting()
        self.counter.increment_count()
        self.assertEqual(self.counter.get_count(), 1)

    def test_count_decrement(self):
        self.counter.start_counting()
        self.counter.increment_count()
        self.counter.decrement_count()
        self.assertEqual(self.counter.get_count(), 0)

if __name__ == '__main__':
    unittest.main()