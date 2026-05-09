# Task 2: Bubble Sort with Pass Tracing

def bubble_sort_trace(arr):
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
        print(f"Pass {i + 1}: {a}")
    return a

lst = [64, 34, 25, 12, 22, 11, 90]
print("Original List:", lst)
bubble_sort_trace(lst)