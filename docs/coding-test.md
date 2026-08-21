# 코딩테스트 학습 노트 (한 파일)

프로그래머스·기업 코딩테스트에서 나오는 **유형 / 문제 원문 / 코드**를 한곳에 모았습니다. SQL과 개념 문제도 이 파일에 있습니다.

공식 사이트 문제 문장은 저작권 때문에 복사하지 않았습니다. 같은 유형을 연습할 수 있는 **학습용 원문**입니다. 실제 기출은 [프로그래머스 고득점 Kit](https://school.programmers.co.kr/learn/challenges?tab=algorithm_practice_kit)에서 푸세요.

공통 풀이 순서: 제약 읽기 → 유형 판별 → 파이썬 표준 라이브러리 선택 → 예제 손풀이 → 구현 → 빈 입력·1-based 확인.

---

## 목차

1. [알고리즘](#알고리즘)
2. [SQL](#sql)
3. [개념](#개념)

---

# 알고리즘

## 1. 해시

**유형:** 해시 / 빈도 카운트  
**판별:** 등장 횟수, 짝 맞추기, 빠른 조회. `Counter` 또는 `dict`.

### 문제. 출석 명단

참가 명단 `joined`와 완주 명단 `finished`가 있습니다. 두 명단은 이름 문자열 배열입니다. 완주하지 못한 사람은 정확히 한 명입니다. 동명이인이 있을 수 있습니다. 완주하지 못한 사람의 이름을 반환하세요.

- `joined` 길이 1 이상 100,000 이하
- `finished` 길이는 `joined`보다 1 작음

**입출력 예**

| joined | finished | 결과 |
| --- | --- | --- |
| `["leo", "kiki", "eden"]` | `["eden", "kiki"]` | `"leo"` |
| `["m", "s", "m", "ana"]` | `["ana", "m", "s"]` | `"m"` |

```python
from collections import Counter

def solution(joined, finished):
    leftover = Counter(joined)
    leftover.subtract(finished)
    for name, cnt in leftover.items():
        if cnt:
            return name
```

**다른 답:** 두 배열을 정렬한 뒤 처음으로 다른 원소. 마지막이 미완주면 `joined[-1]`.

---

## 2. 스택

**유형:** 스택 / 짝 맞추기  
**판별:** 최근 열린 것을 먼저 닫음. `list.append/pop`.

### 문제. 괄호 검사

`'()', '[]', '{}'`만 있는 문자열 `s`가 올바른 괄호열이면 `True`, 아니면 `False`를 반환하세요. 빈 문자열은 올바릅니다.

**입출력 예**

| s | 결과 |
| --- | --- |
| `"{[()]}"` | `True` |
| `"([)]"` | `False` |
| `""` | `True` |

```python
def solution(s):
    pair = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pair:
            if not stack or stack[-1] != pair[ch]:
                return False
            stack.pop()
    return not stack
```

**다른 답:** 재귀적으로 가장 안쪽 쌍을 지움. 느리고 실수하기 쉽습니다.

---

## 3. 큐

**유형:** 큐 / 배포 묶음  
**판별:** 앞 작업이 끝나야 뒤 작업이 나감. `deque` 또는 기준일 카운트.

### 문제. 기능 배포

각 기능의 진도 `progress`(0~99)와 하루 속도 `speeds`가 주어집니다. 하루에 한 번, 진도가 100 이상인 **앞쪽 기능들만** 한꺼번에 배포합니다. 뒤 기능은 앞이 배포될 때까지 기다립니다. 배포마다 몇 개가 나가는지 배열로 반환하세요.

**입출력 예**

| progress | speeds | 결과 |
| --- | --- | --- |
| `[40, 40, 40]` | `[10, 10, 10]` | `[3]` |
| `[90, 80]` | `[5, 5]` | `[1, 1]` |

```python
def solution(progress, speeds):
    days = [((99 - p) + s) // s for p, s in zip(progress, speeds)]
    answer, current, count = [], days[0], 0
    for day in days:
        if day <= current:
            count += 1
        else:
            answer.append(count)
            current, count = day, 1
    answer.append(count)
    return answer
```

**다른 답:** `deque`에 남은 일수를 넣고 앞에서 꺼내기.

---

## 4. 힙

**유형:** 힙 / 우선순위 큐  
**판별:** 매번 최솟값 두 개를 섞음. `heapq`는 최소 힙.

### 문제. 스코빌 섞기

음식 스코빌 지수 배열 `scoville`과 목표 `k`가 있습니다. 가장 맵지 않은 두 음식을 `가장 안 매운 것 + 2 * 그다음`으로 섞습니다. 모든 음식이 `k` 이상이 될 때까지 섞은 횟수를 반환하세요. 불가능하면 `-1`.

**입출력 예**

| scoville | k | 결과 |
| --- | --- | --- |
| `[1, 1, 1]` | `4` | `2` |

```python
import heapq

def solution(scoville, k):
    heapq.heapify(scoville)
    mix = 0
    while len(scoville) >= 2 and scoville[0] < k:
        a = heapq.heappop(scoville)
        b = heapq.heappop(scoville)
        heapq.heappush(scoville, a + 2 * b)
        mix += 1
    return mix if scoville and scoville[0] >= k else -1
```

**다른 답:** 정렬을 매번 하면 O(n² log n)이라 큰 n에서 실패합니다.

---

## 5. 정렬

**유형:** 정렬 / 구간 K번째  
**판별:** 자르고 정렬한 뒤 k번째. 인덱스가 1부터인지 확인.

### 문제. 잘라서 K번째

배열 `array`와 명령 `commands`가 있습니다. 각 명령 `[i, j, k]`는 `array`의 i번째부터 j번째까지 자르고 정렬한 뒤 k번째 수를 고릅니다. 모든 명령의 결과를 배열로 반환하세요. i, j, k는 **1부터** 셉니다.

**입출력 예**

| array | commands | 결과 |
| --- | --- | --- |
| `[4, 3, 2, 1]` | `[[1, 4, 2], [2, 3, 1]]` | `[2, 2]` |

```python
def solution(array, commands):
    return [sorted(array[i - 1 : j])[k - 1] for i, j, k in commands]
```

**다른 답:** `heapq.nsmallest(k, slice)[-1]`. 짧은 구간에서는 정렬이 더 단순합니다.

---

## 6. 완전탐색

**유형:** 완전탐색 / 순열  
**판별:** n이 작고 모든 배치를 봐야 함. `itertools.permutations`.

### 문제. 숫자 조각으로 소수

숫자 문자열 `numbers`의 조각을 붙여 만들 수 있는 **서로 다른 소수**의 개수를 반환하세요. 앞의 0은 정수로 바꿀 때 사라집니다. 예: `"011"` → 11.

**입출력 예**

| numbers | 결과 |
| --- | --- |
| `"2"` | `1` |
| `"23"` | `3`  (2, 3, 23) |

```python
from itertools import permutations

def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

def solution(numbers):
    seen = set()
    for length in range(1, len(numbers) + 1):
        for parts in permutations(numbers, length):
            seen.add(int("".join(parts)))
    return sum(1 for value in seen if is_prime(value))
```

**다른 답:** 백트래킹 + 방문 비트. 중복 숫자는 `set`이 필수입니다.

---

## 7. 탐욕법

**유형:** 그리디 / 투 포인터  
**판별:** 가장 무거운 사람부터 태우고, 가능하면 가벼운 사람을 같이.

### 문제. 구명보트

사람들의 몸무게 `people`와 보트 무게 한도 `limit`가 있습니다. 보트에는 최대 두 명까지 탑니다. 필요한 보트 수의 최솟값을 반환하세요.

**입출력 예**

| people | limit | 결과 |
| --- | --- | --- |
| `[30, 40, 50]` | `70` | `2` |

```python
def solution(people, limit):
    people = sorted(people)
    left, right, boats = 0, len(people) - 1, 0
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1
        right -= 1
        boats += 1
    return boats
```

**다른 답:** 무거운 사람만 혼자 태우면 최솟값이 아닙니다.

---

## 8. 동적계획법

**유형:** DP / 경로 최댓값  
**판별:** 아래층 두 칸 중 큰 값 + 현재 칸.

### 문제. 숫자 삼각형

이차원 리스트 `triangle`에서 맨 위부터 한 칸씩 내려옵니다. 아래층의 **인접한 두 칸** 중 하나로만 갈 수 있습니다. 거쳐 간 숫자의 합 최댓값을 반환하세요.

**입출력 예**

| triangle | 결과 |
| --- | --- |
| `[[1], [2, 3]]` | `4` |

```python
def solution(triangle):
    dp = triangle[-1][:]
    for row in range(len(triangle) - 2, -1, -1):
        for col, value in enumerate(triangle[row]):
            dp[col] = value + max(dp[col], dp[col + 1])
        dp.pop()
    return dp[0]
```

**다른 답:** 위에서 내려가면 경계 처리가 더 깁니다. 아래에서 올라가는 편이 단순합니다.

---

## 9. DFS/BFS

**유형:** DFS / 부호 조합  
**판별:** 각 숫자에 + 또는 −. 최단이 아니면 DFS, 최단이면 BFS.

### 문제. 타겟 만들기

정수 배열 `numbers`의 각 수 앞에 + 또는 −를 붙여 합이 `target`이 되는 경우의 수를 반환하세요.

**입출력 예**

| numbers | target | 결과 |
| --- | --- | --- |
| `[1, 2]` | `1` | `1`  (`-1+2`) |

```python
def solution(numbers, target):
    ways = 0

    def dfs(i, total):
        nonlocal ways
        if i == len(numbers):
            if total == target:
                ways += 1
            return
        dfs(i + 1, total + numbers[i])
        dfs(i + 1, total - numbers[i])

    dfs(0, 0)
    return ways
```

**다른 답:** BFS로 `(index, total)`를 큐에 넣기. n이 20 이하면 둘 다 됩니다.

---

## 10. 이분탐색

**유형:** 파라메트릭 서치  
**판별:** “시간 t면 n명을 처리할 수 있는가?”가 단조 증가.

### 문제. 심사 대기

심사관별 처리 시간 `times`와 사람 수 `n`이 있습니다. 모든 사람이 심사를 끝내는 최소 시간을 반환하세요. 한 심사관은 한 번에 한 명만 봅니다.

**입출력 예**

| times | n | 결과 |
| --- | --- | --- |
| `[2, 3]` | `2` | `3` |

```python
def solution(times, n):
    lo, hi = 1, max(times) * n
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(mid // t for t in times) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

**다른 답:** 우선순위 큐로 시뮬레이션. n이 크면 이분이 더 안전합니다.

---

## 11. 그래프

**유형:** 그래프 BFS / 최단 거리  
**판별:** 가중치 없는 간선, 1번에서 가장 먼 노드 개수.

### 문제. 가장 먼 정점

정점 `n`개(1번부터 n번)와 양방향 간선 `edges`가 있습니다. 1번에서 **최단 경로 기준**으로 가장 멀리 있는 정점의 개수를 반환하세요.

**입출력 예**

| n | edges | 결과 |
| --- | --- | --- |
| `4` | `[[1, 2], [2, 3], [1, 4]]` | `1`  (3번이 거리 2) |

```python
from collections import defaultdict, deque

def solution(n, edges):
    graph = defaultdict(list)
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
    far = max(dist)
    return sum(1 for d in dist if d == far)
```

**다른 답:** DFS는 최단 거리를 보장하지 않습니다.

---

## 12. 구현

**유형:** 구현 / 격자 회전  
**판별:** 시키는 대로 돌리기. 삼성 코테 기본기.

### 문제. 시계 방향 90도

정사각 격자 `grid`를 시계 방향으로 90도 돌린 새 격자를 반환하세요.

**입출력 예**

| grid | 결과 |
| --- | --- |
| `[[1, 2], [3, 4]]` | `[[3, 1], [4, 2]]` |

```python
def solution(grid):
    return [list(row) for row in zip(*grid[::-1])]
```

**다른 답:** `new[j][n-1-i] = grid[i][j]` 직접 대입.

---

## 13. 문자열

**유형:** 문자열 / 압축  
**판별:** 연속 같은 문자 개수.

### 문제. 연속 압축

문자열 `s`에서 같은 문자가 연속되면 `문자+횟수`로 줄입니다. 한 번만 나온 문자는 숫자 없이 문자만 남깁니다. 예: `aaabbc` → `a3b2c`.

```python
def solution(s):
    if not s:
        return ""
    out, prev, cnt = [], s[0], 1
    for ch in s[1:]:
        if ch == prev:
            cnt += 1
        else:
            out.append(prev if cnt == 1 else f"{prev}{cnt}")
            prev, cnt = ch, 1
    out.append(prev if cnt == 1 else f"{prev}{cnt}")
    return "".join(out)
```

---

## 14. 투 포인터 · 슬라이딩 윈도우

**유형:** 투 포인터 / 고정 윈도우  
**판별:** 정렬된 두 수의 합, 또는 길이 k 구간 합.

### 문제 A. 합이 target인 쌍

오름차순 배열 `nums`에 합이 `target`인 서로 다른 두 수가 있으면 `True`.

```python
def solution(nums, target):
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
```

### 문제 B. 길이 k 최대 합

```python
def solution(nums, k):
    current = sum(nums[:k])
    best = current
    for i in range(k, len(nums)):
        current += nums[i] - nums[i - k]
        best = max(best, current)
    return best
```

---

# SQL

프로그래머스 SQL Kit 흐름(SELECT → 집계 → GROUP BY → JOIN → 문자열/날짜)에 맞춘 학습용 원문입니다. 방언은 일반적인 표준 SQL에 가깝게 적었습니다.

공통 스키마:

```sql
-- employees(id, name, dept_id, salary, hired_at)
-- departments(id, name)
-- orders(id, user_id, amount, ordered_at)
-- users(id, name, joined_at)
```

## 15. SELECT · WHERE

**유형:** SQL / 필터

### 문제. 고액 연봉자

`employees`에서 연봉이 5000 이상인 직원의 이름과 연봉을 연봉 내림차순으로 조회하세요.

```sql
SELECT name, salary
FROM employees
WHERE salary >= 5000
ORDER BY salary DESC;
```

---

## 16. 집계 · GROUP BY

**유형:** SQL / GROUP BY · HAVING

### 문제. 부서별 평균 연봉

부서별 평균 연봉을 구하되, 평균이 4000 이상인 부서만 남기고 평균 연봉 내림차순으로 출력하세요. 컬럼명은 `dept_id`, `avg_salary`.

```sql
SELECT dept_id, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) >= 4000
ORDER BY avg_salary DESC;
```

**다른 답:** 부서 이름이 필요하면 `departments`와 JOIN 후 `GROUP BY d.id, d.name`.

---

## 17. JOIN

**유형:** SQL / INNER JOIN · LEFT JOIN

### 문제. 직원과 부서명

모든 직원 이름과 부서명을 출력하세요. 부서가 없는 직원도 이름만 나와야 합니다.

```sql
SELECT e.name AS employee, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

### 문제. 한 번도 주문하지 않은 회원

```sql
SELECT u.id, u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

---

## 18. 문자열 · 날짜

**유형:** SQL / 문자열 · 날짜

### 문제. 2024년 가입자

2024년에 가입한 회원 수를 구하세요.

```sql
SELECT COUNT(*) AS cnt
FROM users
WHERE joined_at >= '2024-01-01'
  AND joined_at <  '2025-01-01';
```

### 문제. 이름에 'kim'이 들어간 직원 (대소문자 무시)

```sql
SELECT name
FROM employees
WHERE LOWER(name) LIKE '%kim%';
```

---

## 19. 윈도우 함수

**유형:** SQL / WINDOW

### 문제. 부서 내 연봉 순위

같은 부서 안에서 연봉 높은 순 순위를 붙이세요. 동점은 같은 순위, 다음 순위는 건너뛰지 않습니다(`DENSE_RANK`).

```sql
SELECT
    name,
    dept_id,
    salary,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
FROM employees;
```

### 문제. 회원별 최근 주문 1건

```sql
SELECT user_id, id, amount, ordered_at
FROM (
    SELECT
        o.*,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY ordered_at DESC) AS rn
    FROM orders o
) t
WHERE rn = 1;
```

---

## 20. 서브쿼리

**유형:** SQL / 서브쿼리

### 문제. 전체 평균보다 연봉이 높은 직원

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

---

# 개념

서술형·단답형입니다. 면접과 코딩테스트 객관식에서 같이 나옵니다.

## 21. 시간 복잡도

**유형:** 개념 / 복잡도

### 문제

배열 길이 n=100,000이고 시간 제한 1초일 때, 이중 루프 O(n²)으로 풀어도 됩니까? 이유를 쓰세요.

**답:** 안 됩니다. 10¹⁰ 번에 가까운 연산이라 1초(대략 10⁷~10⁸)를 넘습니다. O(n log n) 또는 O(n)이 필요합니다.

### 문제

다음을 빠른 순서대로 나열하세요: O(n!), O(n log n), O(n²), O(1), O(2ⁿ), O(n).

**답:** O(1) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)

---

## 22. 자료구조

**유형:** 개념 / 자료구조

### 문제

스택과 큐의 차이를 한 문장씩 쓰고, 파이썬에서 큐를 `list.pop(0)`으로 구현하면 안 되는 이유를 쓰세요.

**답:** 스택은 LIFO, 큐는 FIFO입니다. `list.pop(0)`은 앞을 지울 때마다 O(n)이라 `collections.deque.popleft()`를 씁니다.

### 문제

해시 충돌이란 무엇이고, 파이썬 `dict`는 평균적으로 왜 O(1)입니까?

**답:** 서로 다른 키가 같은 버킷에 들어가는 현상입니다. 평균적으로 버킷이 잘 흩어져 한 번에 접근합니다. 최악은 한 체인에 몰리면 O(n)입니다.

### 문제

최소 힙에서 최솟값 조회와 삽입의 복잡도는?

**답:** 조회 O(1), 삽입·삭제 O(log n).

---

## 23. 운영체제

**유형:** 개념 / OS

### 문제

프로세스와 스레드의 차이를 쓰세요.

**답:** 프로세스는 실행 단위로 주소 공간이 분리됩니다. 스레드는 한 프로세스 안의 실행 흐름으로 메모리(힙·코드)를 공유하고 스택은 각자 가집니다.

### 문제

교착 상태(deadlock)의 필요 조건 4가지를 쓰세요.

**답:** 상호 배제, 점유와 대기, 비선점, 원형 대기.

### 문제

컨텍스트 스위칭이 비싼 이유를 한 줄로 쓰세요.

**답:** CPU 레지스터·프로그램 카운터·메모리 맵을 저장·복원하는 비용이 들기 때문입니다.

---

## 24. 네트워크

**유형:** 개념 / 네트워크

### 문제

HTTP GET과 POST의 차이를 쓰세요.

**답:** GET은 조회용이고 본문 없이 쿼리로 전달하며 캐시될 수 있습니다. POST는 생성·제출용으로 본문에 데이터를 넣고 보통 캐시하지 않습니다.

### 문제

TCP와 UDP의 차이를 쓰세요.

**답:** TCP는 연결형·신뢰 전송(순서, 재전송). UDP는 비연결·빠르지만 손실 가능. 스트리밍·DNS에 UDP를 자주 씁니다.

### 문제

HTTPS가 HTTP보다 안전한 이유를 쓰세요.

**답:** TLS로 암호화·무결성·서버 인증서를 제공합니다.

---

## 25. 데이터베이스

**유형:** 개념 / DB

### 문제

트랜잭션 ACID를 한 줄씩 쓰세요.

**답:**

- Atomicity: 모두 반영되거나 모두 취소
- Consistency: 제약 조건을 깨지 않음
- Isolation: 동시에 실행해도 서로 간섭을 통제
- Durability: 커밋 후 장애가 나도 남음

### 문제

인덱스를 넣으면 항상 빨라집니까?

**답:** 아닙니다. 조회는 빨라질 수 있지만 삽입·갱신·삭제는 인덱스 유지 비용이 듭니다. 카디널리티가 낮으면 효과가 작습니다.

### 문제

정규화의 목적과 역정규화를 하는 이유를 쓰세요.

**답:** 정규화는 중복을 줄여 갱신 이상을 막습니다. 역정규화는 조인을 줄여 읽기 성능을 얻기 위해 중복을 허용합니다.

---

## 26. 파이썬

**유형:** 개념 / 파이썬

### 문제

`[[0] * m] * n`으로 2차원 배열을 만들면 안 되는 이유를 쓰세요.

**답:** 안쪽 리스트가 n번 복사되는 것이 아니라 **같은 객체**를 가리킵니다. `[[0] * m for _ in range(n)]`을 씁니다.

### 문제

리스트와 튜플의 차이를 쓰세요.

**답:** 리스트는 가변, 튜플은 불변이라 `dict` 키가 될 수 있고 약간 더 가볍습니다.

### 문제

GIL이 무엇인가를 한 줄로 쓰세요.

**답:** CPython에서 한 프로세스의 바이트코드는 한 스레드만 실행하게 막는 잠금입니다. CPU  Bound 병렬은 멀티프로세싱이 맞습니다.

---

## 27. 코딩테스트 전략

**유형:** 개념 / 전략

### 문제

n ≤ 10, n ≤ 20, n ≤ 1,000, n ≤ 100,000일 때 각각 어떤 복잡도를 목표로 합니까?

**답:**

- n≤10: O(n!) 순열 가능
- n≤20: O(2ⁿ) 비트마스크·백트래킹
- n≤1,000: O(n²) 가능, O(n³)은 아슬아슬
- n≤100,000: O(n log n) 또는 O(n)

### 문제

BFS와 DFS를 언제 고릅니까?

**답:** 가중치 없는 최단 거리·최소 횟수는 BFS. 모든 경로, 조합, 백트래킹은 DFS.

---

실행 가능한 같은 템플릿은 `src/coding_test/templates.py`에 있고, 테스트는 아래입니다.

```bash
python3 -m unittest discover -s tests -v
```
