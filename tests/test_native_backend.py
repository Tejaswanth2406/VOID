import math
import os
import unittest


os.environ["VOID_NATIVE_BACKEND"] = "python"

from utils.native_backend import reachable_reality_score


class NativeBackendTests(unittest.TestCase):
    def test_python_fallback_matches_score_formula(self):
        connectivity = 11 / (10 * 9 / 2)
        expected = math.log1p(10) * math.log1p(4) * (1 + connectivity) * 0.8 * (1 + math.log1p(2))
        actual = reachable_reality_score(10, 4, 11, 0.8, 2)
        self.assertAlmostEqual(actual, expected)

    def test_empty_space_has_zero_score(self):
        self.assertEqual(reachable_reality_score(0, 8, 0, 1.0, 0), 0.0)


if __name__ == "__main__":
    unittest.main()