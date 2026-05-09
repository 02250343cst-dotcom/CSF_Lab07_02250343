# Task 7: Algorithm Comparison

import time
import tracemalloc

# ── Instrumented Bubble Sort ──────────────────
def bubble_sort_count(arr):
    a = arr[:]
    comps = swaps = 0
    for i in range(len(a) - 1):
        for j in range(len(a) - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
    return a, comps, swaps

# ── Instrumented Insertion Sort ───────────────
def insertion_sort_count(arr):
    a = arr[:]
    comps = swaps = 0
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > key:
                a[j + 1] = a[j]
                swaps += 1
                j -= 1
            else:
                break
        a[j + 1] = key
    return a, comps, swaps

# ── Instrumented Quick Sort ───────────────────
def quick_sort_count(arr, comps, swaps):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left, middle, right = [], [], []
    for x in arr:
        comps[0] += 1
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
            swaps[0] += 1
        else:
            middle.append(x)
    return (quick_sort_count(left, comps, swaps)
            + middle
            + quick_sort_count(right, comps, swaps))

# ── Instrumented Merge Sort ───────────────────
def merge_count(left, right, comps, moves):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        comps[0] += 1
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1; moves[0] += 1
    result.extend(left[i:]); result.extend(right[j:])
    return result

def merge_sort_count(arr, comps, moves):
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    left  = merge_sort_count(arr[:mid], comps, moves)
    right = merge_sort_count(arr[mid:], comps, moves)
    return merge_count(left, right, comps, moves)

# ── Plain sort functions for timing ──────────
def bubble_sort(arr):
    a = arr[:]
    for i in range(len(a) - 1):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def insertion_sort(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]; j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = key
    return a

def quick_sort(arr):
    if len(arr) <= 1: return arr
    p = arr[len(arr) // 2]
    return quick_sort([x for x in arr if x < p]) + \
           [x for x in arr if x == p] + \
           quick_sort([x for x in arr if x > p])

def merge_sort(arr):
    if len(arr) <= 1: return arr
    mid = len(arr) // 2
    l, r = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    res, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if l[i] <= r[j]: res.append(l[i]); i += 1
        else:            res.append(r[j]); j += 1
    return res + l[i:] + r[j:]

# ── Run comparison ────────────────────────────
dataset = [64, 34, 25, 12, 22, 11, 90, 45, 78, 5]
print(f"Dataset: {dataset}\n")

algorithms = [
    ("Bubble Sort",    bubble_sort,    bubble_sort_count),
    ("Insertion Sort", insertion_sort, insertion_sort_count),
]

results = {}

for name, plain_fn, count_fn in algorithms:
    _, comps, swaps = count_fn(dataset[:])

    tracemalloc.start()
    t0 = time.perf_counter()
    for _ in range(1000):
        plain_fn(dataset[:])
    elapsed = (time.perf_counter() - t0) / 1000
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    results[name] = (comps, swaps, elapsed * 1000, peak / 1024)

# Quick Sort
c, s = [0], [0]
quick_sort_count(dataset[:], c, s)
tracemalloc.start()
t0 = time.perf_counter()
for _ in range(1000):
    quick_sort(dataset[:])
elapsed = (time.perf_counter() - t0) / 1000
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
results["Quick Sort"] = (c[0], s[0], elapsed * 1000, peak / 1024)

# Merge Sort
c, m = [0], [0]
merge_sort_count(dataset[:], c, m)
tracemalloc.start()
t0 = time.perf_counter()
for _ in range(1000):
    merge_sort(dataset[:])
elapsed = (time.perf_counter() - t0) / 1000
_, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()
results["Merge Sort"] = (c[0], m[0], elapsed * 1000, peak / 1024)

# ── Print table ───────────────────────────────
print(f"{'Algorithm':<18} {'Comparisons':>12} {'Swaps':>8} {'Time (ms)':>12} {'Mem (KB)':>10}")
print("-" * 65)
for algo, (comps, swaps, ms, kb) in results.items():
    print(f"{algo:<18} {comps:>12} {swaps:>8} {ms:>11.4f}  {kb:>9.3f}")