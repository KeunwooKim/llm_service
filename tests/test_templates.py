from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from coding_test.templates import (
    LRUCache,
    admit_requests,
    agents_can_run,
    batch_complete,
    boats_for_people,
    cheapest_model,
    count_unmatched,
    farthest_count,
    is_valid_brackets,
    kth_in_slices,
    longest_under_limit,
    max_window_sum,
    min_days_to_pass,
    mix_until_k,
    next_job,
    prime_from_digits,
    rotate_right,
    shortest_latency,
    target_ways,
    triangle_max_path,
    two_sum_sorted,
    window_success,
)


class HashTests(unittest.TestCase):
    def test_count_unmatched(self) -> None:
        self.assertEqual(count_unmatched(["a", "b", "b"], ["a", "b"]), 1)


class StackQueueTests(unittest.TestCase):
    def test_brackets(self) -> None:
        self.assertTrue(is_valid_brackets("{[()]}"))
        self.assertFalse(is_valid_brackets("([)]"))

    def test_batch_complete(self) -> None:
        self.assertEqual(batch_complete([40, 40, 40], [10, 10, 10]), [3])
        self.assertEqual(batch_complete([90, 80], [5, 5]), [1, 1])


class HeapSortTests(unittest.TestCase):
    def test_mix_until_k(self) -> None:
        self.assertEqual(mix_until_k([1, 1, 1], 4), 2)

    def test_kth_in_slices(self) -> None:
        self.assertEqual(kth_in_slices([4, 3, 2, 1], [[1, 4, 2], [2, 3, 1]]), [2, 2])


class SearchGreedyDpTests(unittest.TestCase):
    def test_prime_from_digits(self) -> None:
        self.assertEqual(prime_from_digits("2"), 1)
        self.assertEqual(prime_from_digits("23"), 3)

    def test_boats(self) -> None:
        self.assertEqual(boats_for_people([30, 40, 50], 70), 2)

    def test_triangle(self) -> None:
        self.assertEqual(triangle_max_path([[1], [2, 3]]), 4)

    def test_target_ways(self) -> None:
        self.assertEqual(target_ways([1, 2], 1), 1)

    def test_min_days(self) -> None:
        self.assertEqual(min_days_to_pass([2, 3], 2), 3)

    def test_farthest(self) -> None:
        self.assertEqual(farthest_count(4, [[1, 2], [2, 3], [1, 4]]), 1)


class ExtraPatternTests(unittest.TestCase):
    def test_two_sum_sorted(self) -> None:
        self.assertTrue(two_sum_sorted([1, 2, 4, 7], 6))
        self.assertFalse(two_sum_sorted([1, 2, 4, 7], 10))

    def test_window(self) -> None:
        self.assertEqual(max_window_sum([2, 1, 5, 1, 3, 2], 3), 9)

    def test_rotate(self) -> None:
        self.assertEqual(rotate_right([[1, 2], [3, 4]]), [[3, 1], [4, 2]])


class AgentPlatformTests(unittest.TestCase):
    def test_agents_can_run(self) -> None:
        self.assertTrue(agents_can_run(3, [[1, 0], [2, 1]]))
        self.assertFalse(agents_can_run(2, [[0, 1], [1, 0]]))

    def test_lru(self) -> None:
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        cache.put(3, 30)
        self.assertEqual(cache.get(2), -1)

    def test_rate_limit(self) -> None:
        self.assertEqual(admit_requests([1, 1, 1, 2], 2), [True, True, False, True])

    def test_cheapest_model(self) -> None:
        self.assertEqual(cheapest_model([[10, 5, 1], [3, 9, 1], [3, 4, 0]]), 1)
        self.assertEqual(cheapest_model([[8, 1, 0], [8, 2, 0]]), -1)

    def test_window_success(self) -> None:
        self.assertEqual(window_success([[1, 1], [2, 0], [4, 1]], 2), [1.0, 0.5, 1.0])

    def test_longest_under_limit(self) -> None:
        self.assertEqual(longest_under_limit([2, 3, 1, 2, 4], 8), 4)

    def test_next_job(self) -> None:
        self.assertEqual(next_job([[2, 10, 7], [1, 20, 3], [1, 5, 9]], {9}), 3)

    def test_shortest_latency(self) -> None:
        self.assertEqual(shortest_latency(3, [[1, 2, 4], [2, 3, 1], [1, 3, 10]]), 5)


if __name__ == "__main__":
    unittest.main()
