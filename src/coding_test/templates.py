"""Reusable Python 3.10+ patterns for coding tests. Original examples only."""

from __future__ import annotations

import heapq
from collections import Counter, defaultdict, deque, OrderedDict
from itertools import permutations


def count_unmatched(have: list[str], need: list[str]) -> int:
    """Hash: leftovers after matching need against have. O(n)."""
    leftover = Counter(have)
    leftover.subtract(need)
    return sum(max(0, v) for v in leftover.values())


def is_valid_brackets(s: str) -> bool:
    """Stack: pair matching. O(n)."""
    pair = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pair:
            if not stack or stack[-1] != pair[ch]:
                return False
            stack.pop()
    return not stack


def batch_complete(progress: list[int], speeds: list[int]) -> list[int]:
    """Queue: later items wait for the front. O(n)."""
    days = [((99 - p) + s) // s for p, s in zip(progress, speeds)]
    answer: list[int] = []
    current = days[0]
    count = 0
    for day in days:
        if day <= current:
            count += 1
        else:
            answer.append(count)
            current = day
            count = 1
    answer.append(count)
    return answer


def mix_until_k(scoville: list[int], k: int) -> int:
    """Heap: repeatedly mix two smallest. O(n log n)."""
    heapq.heapify(scoville)
    mix = 0
    while len(scoville) >= 2 and scoville[0] < k:
        first = heapq.heappop(scoville)
        second = heapq.heappop(scoville)
        heapq.heappush(scoville, first + 2 * second)
        mix += 1
    return mix if scoville and scoville[0] >= k else -1


def kth_in_slices(array: list[int], commands: list[list[int]]) -> list[int]:
    """Sort: slice, sort, pick k. 1-based i, j, k."""
    return [sorted(array[i - 1 : j])[k - 1] for i, j, k in commands]


def prime_from_digits(numbers: str) -> int:
    """Brute force: unique permutations that form primes."""

    def is_prime(n: int) -> bool:
        if n < 2:
            return False
        d = 2
        while d * d <= n:
            if n % d == 0:
                return False
            d += 1
        return True

    seen: set[int] = set()
    for length in range(1, len(numbers) + 1):
        for parts in permutations(numbers, length):
            seen.add(int("".join(parts)))
    return sum(1 for value in seen if is_prime(value))


def boats_for_people(people: list[int], limit: int) -> int:
    """Greedy two-pointer: heaviest with lightest if possible."""
    people = sorted(people)
    left, right = 0, len(people) - 1
    boats = 0
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1
        right -= 1
        boats += 1
    return boats


def triangle_max_path(triangle: list[list[int]]) -> int:
    """DP bottom-up: each cell takes the better child. O(n^2)."""
    if not triangle:
        return 0
    dp = triangle[-1][:]
    for row in range(len(triangle) - 2, -1, -1):
        for col, value in enumerate(triangle[row]):
            dp[col] = value + max(dp[col], dp[col + 1])
        dp.pop()
    return dp[0]


def target_ways(numbers: list[int], target: int) -> int:
    """DFS/BFS: plus/minus combinations that hit target."""
    ways = 0

    def dfs(index: int, total: int) -> None:
        nonlocal ways
        if index == len(numbers):
            if total == target:
                ways += 1
            return
        dfs(index + 1, total + numbers[index])
        dfs(index + 1, total - numbers[index])

    dfs(0, 0)
    return ways


def min_days_to_pass(times: list[int], n: int) -> int:
    """Binary search on the answer: minimum time for n people."""
    lo, hi = 1, max(times) * n
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(mid // t for t in times) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo


def farthest_count(n: int, edges: list[list[int]]) -> int:
    """Graph BFS: how many nodes sit at the max shortest distance from 1."""
    graph: dict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    dist = [-1] * (n + 1)
    dist[1] = 0
    q = deque([1])
    while q:
        cur = q.popleft()
        for nxt in graph[cur]:
            if dist[nxt] == -1:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    farthest = max(dist)
    return sum(1 for d in dist if d == farthest)


def two_sum_sorted(nums: list[int], target: int) -> bool:
    """Two pointers on a sorted array."""
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return True
        if total < target:
            left += 1
        else:
            right -= 1
    return False


def max_window_sum(nums: list[int], k: int) -> int:
    """Sliding window of fixed length k."""
    if k <= 0 or k > len(nums):
        raise ValueError("invalid window")
    current = sum(nums[:k])
    best = current
    for i in range(k, len(nums)):
        current += nums[i] - nums[i - k]
        best = max(best, current)
    return best


def rotate_right(grid: list[list[int]]) -> list[list[int]]:
    """Implementation: 90-degree clockwise rotate."""
    return [list(row) for row in zip(*grid[::-1])]


def agents_can_run(n: int, deps: list[list[int]]) -> bool:
    """Topological sort: True if agent DAG has no cycle."""
    graph = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in deps:
        graph[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(n) if indeg[i] == 0)
    seen = 0
    while q:
        cur = q.popleft()
        seen += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return seen == n


class LRUCache:
    """Prompt/response cache with O(1) get/put."""

    def __init__(self, capacity: int) -> None:
        self.cap = capacity
        self.data: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.data:
            return -1
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key: int, value: int) -> None:
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.cap:
            self.data.popitem(last=False)


def admit_requests(times: list[int], n: int) -> list[bool]:
    """Sliding 1-second window rate limit."""
    window: deque[int] = deque()
    out: list[bool] = []
    for t in times:
        while window and t - window[0] >= 1:
            window.popleft()
        if len(window) < n:
            window.append(t)
            out.append(True)
        else:
            out.append(False)
    return out


def cheapest_model(models: list[list[int]]) -> int:
    """Hybrid router: min cost, then min latency among available models."""
    heap: list[tuple[int, int, int]] = []
    for i, (cost, latency, ok) in enumerate(models):
        if ok:
            heapq.heappush(heap, (cost, latency, i))
    return heap[0][2] if heap else -1


def window_success(events: list[list[int]], k: int) -> list[float]:
    """Recent-k-second success rate after each event."""
    q: deque[tuple[int, int]] = deque()
    success = 0
    out: list[float] = []
    for t, ok in events:
        q.append((t, ok))
        success += ok
        while q and t - q[0][0] >= k:
            _, old = q.popleft()
            success -= old
        total = len(q)
        out.append(0.0 if total == 0 else success / total)
    return out


def longest_under_limit(lens: list[int], limit: int) -> int:
    """RAG chunk: longest subarray whose sum <= limit."""
    left = total = best = 0
    for right, width in enumerate(lens):
        total += width
        while total > limit:
            total -= lens[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def next_job(queue: list[list[int]], busy: set[int]) -> int:
    """Worker pool: smallest (priority, arrived_at) job not in busy."""
    heap: list[tuple[int, int, int]] = []
    for priority, arrived_at, job_id in queue:
        if job_id not in busy:
            heapq.heappush(heap, (priority, arrived_at, job_id))
    return heap[0][2] if heap else -1


def shortest_latency(n: int, edges: list[list[int]]) -> int:
    """Dijkstra from node 1 to n on an undirected weighted graph."""
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    dist = [float("inf")] * (n + 1)
    dist[1] = 0
    heap = [(0, 1)]
    while heap:
        d, cur = heapq.heappop(heap)
        if d > dist[cur]:
            continue
        for nxt, w in graph[cur]:
            nd = d + w
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return -1 if dist[n] == float("inf") else int(dist[n])
