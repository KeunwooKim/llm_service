# 코딩테스트 학습 노트

프로그래머스·기업 코딩테스트에서 나오는 **유형 / 문제 원문 / 코드**를 한곳에 모았습니다. SQL과 개념 문제도 이 파일에 있습니다.

공식 사이트 문제 문장은 저작권 때문에 복사하지 않았습니다. 같은 유형을 연습할 수 있는 **학습용 원문**입니다. 실제 기출은 [프로그래머스 고득점 Kit](https://school.programmers.co.kr/learn/challenges?tab=algorithm_practice_kit)에서 푸세요.

공통 풀이 순서: 제약 읽기 → 유형 판별 → 파이썬 표준 라이브러리 선택 → 예제 손풀이 → 구현 → 빈 입력·1-based 확인.

> 노션에 넣는 방법
> 1. 이 파일을 통째로 복사해 페이지에 붙여넣거나, 노션 Import → Markdown으로 가져옵니다. Import가 표·코드 블록을 더 잘 살립니다.
> 2. 붙여넣은 뒤 `/목차` 를 입력하면 제목(H1~H4) 기준으로 목차가 생깁니다. GitHub용 `#링크`는 노션에서 동작하지 않습니다.
> 3. 유형·판별 줄은 인용 블록입니다. 원하면 `/콜아웃`으로 바꿔도 됩니다.

---

## 목차

- 빠른 찾기
- 알고리즘
  - 1. 해시
    - 문제. 출석 명단
  - 2. 스택
    - 문제. 괄호 검사
  - 3. 큐
    - 문제. 기능 배포
  - 4. 힙
    - 문제. 스코빌 섞기
  - 5. 정렬
    - 문제. 잘라서 K번째
  - 6. 완전탐색
    - 문제. 숫자 조각으로 소수
  - 7. 탐욕법
    - 문제. 구명보트
  - 8. 동적계획법
    - 문제. 숫자 삼각형
  - 9. DFS/BFS
    - 문제. 타겟 만들기
  - 10. 이분탐색
    - 문제. 심사 대기
  - 11. 그래프
    - 문제. 가장 먼 정점
  - 12. 구현
    - 문제. 시계 방향 90도
  - 13. 문자열
    - 문제. 연속 압축
  - 14. 투 포인터 · 슬라이딩 윈도우
    - 문제 A. 합이 target인 쌍
    - 문제 B. 길이 k 최대 합
- SQL
  - 15. SELECT · WHERE
    - 문제. 고액 연봉자
  - 16. 집계 · GROUP BY
    - 문제. 부서별 평균 연봉
  - 17. JOIN
    - 문제. 직원과 부서명
    - 문제. 한 번도 주문하지 않은 회원
  - 18. 문자열 · 날짜
    - 문제. 2024년 가입자
    - 문제. 이름에 'kim'이 들어간 직원 (대소문자 무시)
  - 19. 윈도우 함수
    - 문제. 부서 내 연봉 순위
    - 문제. 회원별 최근 주문 1건
  - 20. 서브쿼리
    - 문제. 전체 평균보다 연봉이 높은 직원
- 개념
  - 21. 시간 복잡도
    - 문제. n=10만에서 O(n²)
    - 문제. 복잡도 빠른 순서
  - 22. 자료구조
    - 문제. 스택 vs 큐
    - 문제. 해시 충돌
    - 문제. 힙 복잡도
  - 23. 운영체제
    - 문제. 프로세스 vs 스레드
    - 문제. 교착 상태 4조건
    - 문제. 컨텍스트 스위칭
  - 24. 네트워크
    - 문제. GET vs POST
    - 문제. TCP vs UDP
    - 문제. HTTPS
  - 25. 데이터베이스
    - 문제. ACID
    - 문제. 인덱스
    - 문제. 정규화
  - 26. 파이썬
    - 문제. 2차원 배열 초기화
    - 문제. 리스트 vs 튜플
    - 문제. GIL
  - 27. 코딩테스트 전략
    - 문제. n 크기별 복잡도
    - 문제. BFS vs DFS
- XGEN·에이전틱 AI 직무 코테
  - 28. 에이전트 파이프라인 DAG
    - 문제. 에이전트 실행 가능 여부
  - 29. 프롬프트 LRU 캐시
    - 문제. 용량 제한 캐시
  - 30. LLM API 토큰 버킷
    - 문제. 초당 최대 N회
  - 31. 하이브리드 모델 라우터
    - 문제. 가장 싼 사용 가능 모델
  - 32. 실시간 예측 로그 윈도우
    - 문제. 최근 k초 성공률
  - 33. RAG 청크
    - 문제. 최대 길이 이하로 자르기
  - 34. 추론 작업 대기열
    - 문제. 다음 잡을 고르기
  - 35. 모델 엔드포인트 최단 지연
    - 문제. 1번에서 n번까지
  - 36. SQL — 모델별 토큰·지연
    - 문제. 모델별 호출 수, 평균 토큰, 성공률
    - 문제. 모델별 지연 상위 5% 근처 (윈도우)
  - 37. 개념 — 이 직무 면접/코테 서술
    - 문제. LangChain/LangGraph에서 노드와 엣지는 코딩테스트의 무엇과 같습니까?
    - 문제. MLOps와 LLMOps의 차이를 세 줄로 쓰세요.
    - 문제. 하이브리드 LLM 오케스트레이션에서 라우팅 기준 세 가지를 쓰세요.
    - 문제. 대용량 실시간 파이프라인에서 왜 슬라이딩 윈도우를 씁니까?
    - 문제. 오픈소스 프레임워크를 “재사용성 높게 추상화”한다는 것은 코테에서 어떻게 보입니까?

### 빠른 찾기

| 키워드 | 문제 |
| --- | --- |
| 해시, Counter, 동명이인 | 출석 명단 |
| 괄호, 스택 | 괄호 검사 |
| 큐, 배포 | 기능 배포 |
| 힙, 우선순위 | 스코빌 섞기 |
| 정렬, K번째 | 잘라서 K번째 |
| 순열, 소수, 완전탐색 | 숫자 조각으로 소수 |
| 그리디, 투 포인터 | 구명보트 |
| DP | 숫자 삼각형 |
| DFS/BFS | 타겟 만들기 |
| 이분탐색 | 심사 대기 |
| 그래프 BFS | 가장 먼 정점 |
| 격자 회전 | 시계 방향 90도 |
| 문자열 압축 | 연속 압축 |
| 투 포인터 | 합이 target인 쌍 |
| 슬라이딩 윈도우 | 길이 k 최대 합 |
| SQL SELECT | 고액 연봉자 |
| GROUP BY | 부서별 평균 연봉 |
| JOIN | 직원과 부서명 |
| 윈도우 함수 | 부서 내 연봉 순위 |
| 복잡도 | n=10만에서 O(n²) |
| OS | 프로세스 vs 스레드 |
| 네트워크 | GET vs POST |
| DB | ACID |
| 파이썬 함정 | 2차원 배열 초기화 |
| 에이전트 DAG | 에이전트 실행 가능 여부 |
| LRU 캐시 | 용량 제한 캐시 |
| 레이트리밋 | 초당 최대 N회 |
| 모델 라우팅 | 가장 싼 사용 가능 모델 |
| 실시간 로그 | 최근 k초 성공률 |
| RAG 청크 | 최대 길이 이하로 자르기 |
| 작업 큐 | 다음 잡을 고르기 |
| 다익스트라 | 1번에서 n번까지 |
| LLMOps 개념 | MLOps와 LLMOps |

---

## 알고리즘

### 1. 해시

> 유형: 해시 / 빈도 카운트
> 판별: 등장 횟수, 짝 맞추기, 빠른 조회. `Counter` 또는 `dict`.

#### 문제. 출석 명단

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

### 2. 스택

> 유형: 스택 / 짝 맞추기
> 판별: 최근 열린 것을 먼저 닫음. `list.append/pop`.

#### 문제. 괄호 검사

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

### 3. 큐

> 유형: 큐 / 배포 묶음
> 판별: 앞 작업이 끝나야 뒤 작업이 나감. `deque` 또는 기준일 카운트.

#### 문제. 기능 배포

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

### 4. 힙

> 유형: 힙 / 우선순위 큐
> 판별: 매번 최솟값 두 개를 섞음. `heapq`는 최소 힙.

#### 문제. 스코빌 섞기

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

### 5. 정렬

> 유형: 정렬 / 구간 K번째
> 판별: 자르고 정렬한 뒤 k번째. 인덱스가 1부터인지 확인.

#### 문제. 잘라서 K번째

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

### 6. 완전탐색

> 유형: 완전탐색 / 순열
> 판별: n이 작고 모든 배치를 봐야 함. `itertools.permutations`.

#### 문제. 숫자 조각으로 소수

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

### 7. 탐욕법

> 유형: 그리디 / 투 포인터
> 판별: 가장 무거운 사람부터 태우고, 가능하면 가벼운 사람을 같이.

#### 문제. 구명보트

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

### 8. 동적계획법

> 유형: DP / 경로 최댓값
> 판별: 아래층 두 칸 중 큰 값 + 현재 칸.

#### 문제. 숫자 삼각형

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

### 9. DFS/BFS

> 유형: DFS / 부호 조합
> 판별: 각 숫자에 + 또는 −. 최단이 아니면 DFS, 최단이면 BFS.

#### 문제. 타겟 만들기

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

### 10. 이분탐색

> 유형: 파라메트릭 서치
> 판별: “시간 t면 n명을 처리할 수 있는가?”가 단조 증가.

#### 문제. 심사 대기

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

### 11. 그래프

> 유형: 그래프 BFS / 최단 거리
> 판별: 가중치 없는 간선, 1번에서 가장 먼 노드 개수.

#### 문제. 가장 먼 정점

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

### 12. 구현

> 유형: 구현 / 격자 회전
> 판별: 시키는 대로 돌리기. 삼성 코테 기본기.

#### 문제. 시계 방향 90도

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

### 13. 문자열

> 유형: 문자열 / 압축
> 판별: 연속 같은 문자 개수.

#### 문제. 연속 압축

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

### 14. 투 포인터 · 슬라이딩 윈도우

> 유형: 투 포인터 / 고정 윈도우
> 판별: 정렬된 두 수의 합, 또는 길이 k 구간 합.

#### 문제 A. 합이 target인 쌍

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

#### 문제 B. 길이 k 최대 합

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

## SQL

프로그래머스 SQL Kit 흐름(SELECT → 집계 → GROUP BY → JOIN → 문자열/날짜)에 맞춘 학습용 원문입니다. 방언은 일반적인 표준 SQL에 가깝게 적었습니다.

공통 스키마:

```sql
-- employees(id, name, dept_id, salary, hired_at)
-- departments(id, name)
-- orders(id, user_id, amount, ordered_at)
-- users(id, name, joined_at)
```

### 15. SELECT · WHERE

> 유형: SQL / 필터

#### 문제. 고액 연봉자

`employees`에서 연봉이 5000 이상인 직원의 이름과 연봉을 연봉 내림차순으로 조회하세요.

```sql
SELECT name, salary
FROM employees
WHERE salary >= 5000
ORDER BY salary DESC;
```

---

### 16. 집계 · GROUP BY

> 유형: SQL / GROUP BY · HAVING

#### 문제. 부서별 평균 연봉

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

### 17. JOIN

> 유형: SQL / INNER JOIN · LEFT JOIN

#### 문제. 직원과 부서명

모든 직원 이름과 부서명을 출력하세요. 부서가 없는 직원도 이름만 나와야 합니다.

```sql
SELECT e.name AS employee, d.name AS department
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id;
```

#### 문제. 한 번도 주문하지 않은 회원

```sql
SELECT u.id, u.name
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.id IS NULL;
```

---

### 18. 문자열 · 날짜

> 유형: SQL / 문자열 · 날짜

#### 문제. 2024년 가입자

2024년에 가입한 회원 수를 구하세요.

```sql
SELECT COUNT(*) AS cnt
FROM users
WHERE joined_at >= '2024-01-01'
  AND joined_at <  '2025-01-01';
```

#### 문제. 이름에 'kim'이 들어간 직원 (대소문자 무시)

```sql
SELECT name
FROM employees
WHERE LOWER(name) LIKE '%kim%';
```

---

### 19. 윈도우 함수

> 유형: SQL / WINDOW

#### 문제. 부서 내 연봉 순위

같은 부서 안에서 연봉 높은 순 순위를 붙이세요. 동점은 같은 순위, 다음 순위는 건너뛰지 않습니다(`DENSE_RANK`).

```sql
SELECT
    name,
    dept_id,
    salary,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
FROM employees;
```

#### 문제. 회원별 최근 주문 1건

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

### 20. 서브쿼리

> 유형: SQL / 서브쿼리

#### 문제. 전체 평균보다 연봉이 높은 직원

```sql
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
```

---

## 개념

서술형·단답형입니다. 면접과 코딩테스트 객관식에서 같이 나옵니다.

### 21. 시간 복잡도

> 유형: 개념 / 복잡도

#### 문제. n=10만에서 O(n²)

배열 길이 n=100,000이고 시간 제한 1초일 때, 이중 루프 O(n²)으로 풀어도 됩니까? 이유를 쓰세요.

**답:** 안 됩니다. 10¹⁰ 번에 가까운 연산이라 1초(대략 10⁷~10⁸)를 넘습니다. O(n log n) 또는 O(n)이 필요합니다.

#### 문제. 복잡도 빠른 순서

다음을 빠른 순서대로 나열하세요: O(n!), O(n log n), O(n²), O(1), O(2ⁿ), O(n).

**답:** O(1) < O(n) < O(n log n) < O(n²) < O(2ⁿ) < O(n!)

---

### 22. 자료구조

> 유형: 개념 / 자료구조

#### 문제. 스택 vs 큐

스택과 큐의 차이를 한 문장씩 쓰고, 파이썬에서 큐를 `list.pop(0)`으로 구현하면 안 되는 이유를 쓰세요.

**답:** 스택은 LIFO, 큐는 FIFO입니다. `list.pop(0)`은 앞을 지울 때마다 O(n)이라 `collections.deque.popleft()`를 씁니다.

#### 문제. 해시 충돌

해시 충돌이란 무엇이고, 파이썬 `dict`는 평균적으로 왜 O(1)입니까?

**답:** 서로 다른 키가 같은 버킷에 들어가는 현상입니다. 평균적으로 버킷이 잘 흩어져 한 번에 접근합니다. 최악은 한 체인에 몰리면 O(n)입니다.

#### 문제. 힙 복잡도

최소 힙에서 최솟값 조회와 삽입의 복잡도는?

**답:** 조회 O(1), 삽입·삭제 O(log n).

---

### 23. 운영체제

> 유형: 개념 / OS

#### 문제. 프로세스 vs 스레드

프로세스와 스레드의 차이를 쓰세요.

**답:** 프로세스는 실행 단위로 주소 공간이 분리됩니다. 스레드는 한 프로세스 안의 실행 흐름으로 메모리(힙·코드)를 공유하고 스택은 각자 가집니다.

#### 문제. 교착 상태 4조건

교착 상태(deadlock)의 필요 조건 4가지를 쓰세요.

**답:** 상호 배제, 점유와 대기, 비선점, 원형 대기.

#### 문제. 컨텍스트 스위칭

컨텍스트 스위칭이 비싼 이유를 한 줄로 쓰세요.

**답:** CPU 레지스터·프로그램 카운터·메모리 맵을 저장·복원하는 비용이 들기 때문입니다.

---

### 24. 네트워크

> 유형: 개념 / 네트워크

#### 문제. GET vs POST

HTTP GET과 POST의 차이를 쓰세요.

**답:** GET은 조회용이고 본문 없이 쿼리로 전달하며 캐시될 수 있습니다. POST는 생성·제출용으로 본문에 데이터를 넣고 보통 캐시하지 않습니다.

#### 문제. TCP vs UDP

TCP와 UDP의 차이를 쓰세요.

**답:** TCP는 연결형·신뢰 전송(순서, 재전송). UDP는 비연결·빠르지만 손실 가능. 스트리밍·DNS에 UDP를 자주 씁니다.

#### 문제. HTTPS

HTTPS가 HTTP보다 안전한 이유를 쓰세요.

**답:** TLS로 암호화·무결성·서버 인증서를 제공합니다.

---

### 25. 데이터베이스

> 유형: 개념 / DB

#### 문제. ACID

트랜잭션 ACID를 한 줄씩 쓰세요.

**답:**

- Atomicity: 모두 반영되거나 모두 취소
- Consistency: 제약 조건을 깨지 않음
- Isolation: 동시에 실행해도 서로 간섭을 통제
- Durability: 커밋 후 장애가 나도 남음

#### 문제. 인덱스

인덱스를 넣으면 항상 빨라집니까?

**답:** 아닙니다. 조회는 빨라질 수 있지만 삽입·갱신·삭제는 인덱스 유지 비용이 듭니다. 카디널리티가 낮으면 효과가 작습니다.

#### 문제. 정규화

정규화의 목적과 역정규화를 하는 이유를 쓰세요.

**답:** 정규화는 중복을 줄여 갱신 이상을 막습니다. 역정규화는 조인을 줄여 읽기 성능을 얻기 위해 중복을 허용합니다.

---

### 26. 파이썬

> 유형: 개념 / 파이썬

#### 문제. 2차원 배열 초기화

`[[0] * m] * n`으로 2차원 배열을 만들면 안 되는 이유를 쓰세요.

**답:** 안쪽 리스트가 n번 복사되는 것이 아니라 **같은 객체**를 가리킵니다. `[[0] * m for _ in range(n)]`을 씁니다.

#### 문제. 리스트 vs 튜플

리스트와 튜플의 차이를 쓰세요.

**답:** 리스트는 가변, 튜플은 불변이라 `dict` 키가 될 수 있고 약간 더 가볍습니다.

#### 문제. GIL

GIL이 무엇인가를 한 줄로 쓰세요.

**답:** CPython에서 한 프로세스의 바이트코드는 한 스레드만 실행하게 막는 잠금입니다. CPU  Bound 병렬은 멀티프로세싱이 맞습니다.

---

### 27. 코딩테스트 전략

> 유형: 개념 / 전략

#### 문제. n 크기별 복잡도

n ≤ 10, n ≤ 20, n ≤ 1,000, n ≤ 100,000일 때 각각 어떤 복잡도를 목표로 합니까?

**답:**

- n≤10: O(n!) 순열 가능
- n≤20: O(2ⁿ) 비트마스크·백트래킹
- n≤1,000: O(n²) 가능, O(n³)은 아슬아슬
- n≤100,000: O(n log n) 또는 O(n)

#### 문제. BFS vs DFS

BFS와 DFS를 언제 고릅니까?

**답:** 가중치 없는 최단 거리·최소 횟수는 BFS. 모든 경로, 조합, 백트래킹은 DFS.

---

## XGEN·에이전틱 AI 직무 코테

아래는 공고의 코어 엔진 / 하이브리드 LLM 오케스트레이션 / 대용량 실시간 처리 / LLMOps 라이프사이클에 맞춰, 외부 글에서 **반복되는 유형**을 학습용 원문으로 재작성한 세트입니다.

유형 참고:

- LangGraph를 DAG·조건부 엣지로 보는 글: [jongkwan.dev](https://jongkwan.dev/posts/langgraph-agent-orchestration), [youngju.dev](https://www.youngju.dev/blog/chatbot/2026-03-05-chatbot-langgraph-multi-agent-production)
- 위상정렬(파이프라인 의존성): [velog Course Schedule](https://velog.io/@pppcent/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EC%9C%84%EC%83%81%EC%A0%95%EB%A0%AC-207.-Course-Schedule-Leetcode)
- 채점/작업 대기열 + 힙: [코드트리 채점기 풀이](https://bloodstrawberry.tistory.com/1543)
- LLMOps 캐시·토큰·모니터링: [NVIDIA LLMOps](https://developer.nvidia.com/ko-kr/blog/mastering-llm-techniques-llmops/), [LLMOps 플랫폼 가이드](https://www.youngju.dev/blog/ai-platform/2026-03-13-llmops-platform-model-deployment-monitoring-ab-testing)

공고 매핑:

| 공고 업무 | 코테에서 묻는 것 |
| --- | --- |
| 하이브리드 LLM 오케스트레이션 | DAG 위상정렬, 조건부 라우팅, 우선순위 큐 |
| 대용량 실시간 예측 | 슬라이딩 윈도우, 스트림 집계, 다익스트라 |
| LLMOps 원스톱 제어 | LRU 캐시, 토큰 버킷, 사용량 SQL |
| 프레임워크 추상화 | 작은 모듈로 재사용 (클래스 설계) |

---

### 28. 에이전트 파이프라인 DAG

> 유형: 그래프 / 위상정렬
> 직무: XGEN 코어 엔진이 에이전트 노드를 순환 없이 실행하는지.

#### 문제. 에이전트 실행 가능 여부

에이전트 `n`개(0 ~ n-1)와 의존성 `deps`가 있습니다. `deps[i] = [a, b]`는 **b가 끝난 뒤에야 a를 실행**할 수 있다는 뜻입니다. 모든 에이전트를 실행할 수 있으면 `True`, 순환이 있으면 `False`를 반환하세요.

**입출력 예**

| n | deps | 결과 |
| --- | --- | --- |
| `3` | `[[1, 0], [2, 1]]` | `True`  (0 → 1 → 2) |
| `2` | `[[0, 1], [1, 0]]` | `False` |

```python
from collections import deque

def solution(n, deps):
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
```

실행 순서까지 필요하면 `order` 리스트에 `cur`를 담으면 됩니다. 순환이면 `len(order) < n`.

---

### 29. 프롬프트 LRU 캐시

> 유형: 해시 + 더블 링크드 리스트 / `OrderedDict`
> 직무: 같은 프롬프트 반복 호출을 캐시해 추론 비용을 줄임.

#### 문제. 용량 제한 캐시

용량 `capacity`인 LRU 캐시를 구현하세요.

- `get(key)`: 있으면 값을 반환하고 최근 사용으로 표시. 없으면 `-1`
- `put(key, value)`: 넣고 최근 사용으로 표시. 용량을 넘으면 **가장 오래 안 쓴** 키를 삭제

**입출력 예**

```
cache = LRUCache(2)
cache.put(1, 10)
cache.put(2, 20)
cache.get(1)      # 10
cache.put(3, 30)  # key 2 삭제
cache.get(2)      # -1
```

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.data = OrderedDict()

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
```

**다른 답:** `dict` + 직접 구현한 양방향 리스트. 면접에서 원리를 물을 때 씁니다.

---

### 30. LLM API 토큰 버킷

> 유형: 큐 / 슬라이딩 윈도우
> 직무: 모델 API 분당 호출 한도, 하이브리드 라우팅 가드레일.

#### 문제. 초당 최대 N회

시간 순서대로 정렬된 요청 시각(초) `times`와 한도 `n`이 있습니다. 같은 1초 구간 `[t, t+1)` 안에 `n`번을 넘긴 요청은 거절입니다. 각 요청을 수락하면 `True`, 거절이면 `False`인 배열을 반환하세요. 거절된 요청은 윈도우에 넣지 않습니다.

**입출력 예**

| times | n | 결과 |
| --- | --- | --- |
| `[1, 1, 1, 2]` | `2` | `[True, True, False, True]` |

```python
from collections import deque

def solution(times, n):
    window = deque()
    out = []
    for t in times:
        while window and t - window[0] >= 1:
            window.popleft()
        if len(window) < n:
            window.append(t)
            out.append(True)
        else:
            out.append(False)
    return out
```

토큰 버킷(초당 r 충전, 버킷 크기 b)은 `tokens = min(b, tokens + (now-prev)*r)` 후 1 감소로 구현합니다.

---

### 31. 하이브리드 모델 라우터

> 유형: 힙
> 직무: 여러 Open-Source/API 모델 중 지연·비용이 낮은 쪽을 고름.

#### 문제. 가장 싼 사용 가능 모델

모델 목록 `models`의 각 원소는 `[cost, latency, available]`입니다. `available`이 1이면 사용 가능. 사용 가능한 모델 중 **비용이 가장 작고**, 동점이면 **지연이 가장 작은** 모델의 인덱스를 반환하세요. 없으면 `-1`.

**입출력 예**

| models | 결과 |
| --- | --- |
| `[[10, 5, 1], [3, 9, 1], [3, 4, 0]]` | `1` |
| `[[8, 1, 0], [8, 2, 0]]` | `-1` |

```python
import heapq

def solution(models):
    heap = []
    for i, (cost, latency, ok) in enumerate(models):
        if ok:
            heapq.heappush(heap, (cost, latency, i))
    return heap[0][2] if heap else -1
```

모델이 동적으로 들어오고 빠지면 힙에 `(cost, latency, id)`를 넣고, 꺼낸 뒤 `available[id]`가 꺼져 있으면 버립니다.

---

### 32. 실시간 예측 로그 윈도우

> 유형: 슬라이딩 윈도우 / 해시
> 직무: genser 실시간 대용량 이벤트에서 최근 k초 성공률.

#### 문제. 최근 k초 성공률

이벤트 `events`는 `[timestamp, success]` (success는 0/1)이고 시간순입니다. 각 이벤트 시점에 **직전 k초 구간 (t-k, t]** 의 성공률(성공/전체)을 소수 둘째 자리까지 버린 뒤 리스트로 반환하세요. 구간이 비면 0.0.

**입출력 예**

| events | k | 결과 |
| --- | --- | --- |
| `[[1, 1], [2, 0], [4, 1]]` | `2` | `[1.0, 0.5, 1.0]` |

코드는 `t - old_t >= k`이면 구간에서 빼므로 열린 구간 `(t-k, t]`와 같습니다.

```python
from collections import deque

def solution(events, k):
    q = deque()
    success = 0
    out = []
    for t, ok in events:
        q.append((t, ok))
        success += ok
        while q and t - q[0][0] >= k:
            _, old = q.popleft()
            success -= old
        total = len(q)
        out.append(0.0 if total == 0 else success / total)
    return out
```

---

### 33. RAG 청크

> 유형: 투 포인터
> 직무: 대용량 문서를 토큰 한도 안으로 자름.

#### 문제. 최대 길이 이하로 자르기

단어 길이 배열 `lens`와 한도 `limit`가 있습니다. 연속 단어의 길이 합이 `limit`을 넘지 않는 **가장 긴 구간 길이**(단어 개수)를 반환하세요.

**입출력 예**

| lens | limit | 결과 |
| --- | --- | --- |
| `[2, 3, 1, 2, 4]` | `8` | `4` |

```python
def solution(lens, limit):
    left = total = best = 0
    for right, w in enumerate(lens):
        total += w
        while total > limit:
            total -= lens[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```

---

### 34. 추론 작업 대기열

> 유형: 힙 + 해시
> 직무: 채점기/워커 풀처럼 우선순위가 높은 잡을 GPU 워커에 배정. (코드트리 채점기 유형을 단순화)

#### 문제. 다음 잡을 고르기

대기열에 `[priority, arrived_at, job_id]`가 쌓입니다. `priority`가 작을수록, 같으면 `arrived_at`이 작을수록 먼저입니다. `busy`인 `job_id`는 고르지 않습니다. 다음에 실행할 `job_id`를 반환하세요. 없으면 `-1`.

**입출력 예**

| queue | busy | 결과 |
| --- | --- | --- |
| `[[2, 10, 7], [1, 20, 3], [1, 5, 9]]` | `{9}` | `3` |

```python
import heapq

def solution(queue, busy):
    heap = []
    for p, t, jid in queue:
        if jid not in busy:
            heapq.heappush(heap, (p, t, jid))
    return heap[0][2] if heap else -1
```

실제 엔진은 도메인별 힙 + 워커 유휴 집합을 같이 둡니다.

---

### 35. 모델 엔드포인트 최단 지연

> 유형: 다익스트라
> 직무: 리전/게이트웨이  hop을 지나 가장 빠른 추론 경로.

#### 문제. 1번에서 n번까지

정점 `n`개, 가중 간선 `edges` (`[u, v, w]` 양방향). 1번에서 n번까지 최소 지연을 반환하세요. 없으면 `-1`.

**입출력 예**

| n | edges | 결과 |
| --- | --- | --- |
| `3` | `[[1, 2, 4], [2, 3, 1], [1, 3, 10]]` | `5` |

```python
import heapq
from collections import defaultdict

def solution(n, edges):
    graph = defaultdict(list)
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
    return -1 if dist[n] == float("inf") else dist[n]
```

---

### 36. SQL — 모델별 토큰·지연

> 유형: SQL / GROUP BY · 윈도우
> 직무: LLMOps 원스톱 모니터링.

스키마: `infer_logs(id, model, tokens, latency_ms, ok, created_at)`

#### 문제. 모델별 호출 수, 평균 토큰, 성공률

오늘 날짜 로그만. 성공률은 `ok=1` 비율.

```sql
SELECT
    model,
    COUNT(*) AS calls,
    AVG(tokens) AS avg_tokens,
    AVG(CASE WHEN ok = 1 THEN 1.0 ELSE 0.0 END) AS success_rate
FROM infer_logs
WHERE created_at >= CURRENT_DATE
  AND created_at <  CURRENT_DATE + INTERVAL '1' DAY
GROUP BY model
ORDER BY calls DESC;
```

#### 문제. 모델별 지연 상위 5% 근처 (윈도우)

표준 SQL에서 퍼센타일은 방언마다 다릅니다. 순위 비율로 근사합니다.

```sql
SELECT model, latency_ms
FROM (
    SELECT
        model,
        latency_ms,
        PERCENT_RANK() OVER (PARTITION BY model ORDER BY latency_ms) AS pr
    FROM infer_logs
) t
WHERE pr >= 0.95;
```

---

### 37. 개념 — 이 직무 면접/코테 서술

> 유형: 개념 / LLMOps · 오케스트레이션

#### 문제. LangChain/LangGraph에서 노드와 엣지는 코딩테스트의 무엇과 같습니까?

**답:** 노드는 함수(에이전트 한 스텝), 일반 엣지는 고정 전이, 조건부 엣지는 상태 분기입니다. 전체는 DAG에 가깝고 순환이 있으면 recursion limit가 필요합니다. 코테의 그래프 + 위상정렬과 같습니다.

#### 문제. MLOps와 LLMOps의 차이를 세 줄로 쓰세요.

**답:** MLOps는 학습·재학습·모델 아티팩트 중심입니다. LLMOps는 프롬프트 버전, RAG/벡터 DB, 토큰당 비용, 가드레일이 중심입니다. 배포 주기도 프롬프트 변경은 분 단위로 짧습니다.

#### 문제. 하이브리드 LLM 오케스트레이션에서 라우팅 기준 세 가지를 쓰세요.

**답:** 품질(평가 점수), 지연(p95), 비용(토큰). 가드레일 실패·타임아웃이면 fallback 모델로 넘깁니다.

#### 문제. 대용량 실시간 파이프라인에서 왜 슬라이딩 윈도우를 씁니까?

**답:** 전체 재집계는 O(N)이 반복되어 못 버팁니다. 구간에서 빠지는 값만 빼고 들어오는 값만 더하면 O(1)에 가깝게 갱신됩니다.

#### 문제. 오픈소스 프레임워크를 “재사용성 높게 추상화”한다는 것은 코테에서 어떻게 보입니까?

**답:** LRU·레이트리밋·라우터처럼 **작은 클래스/함수로 경계를 나누고**, 자료구조 복잡도를 명시하는 설계입니다. 한 함수에 모든 분기를 넣지 않습니다.

---

실행 가능한 같은 템플릿은 `src/coding_test/templates.py`에 있고, 테스트는 아래입니다.

```bash
python3 -m unittest discover -s tests -v
```
