# Task 4: Insertion Sort with Step Tracing

def insertion_sort_trace(arr):
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
        print(f"Pass {i}: {a}")
    return a

lst = [9, 5, 1, 4, 3]
print("Original List:", lst)
insertion_sort_trace(lst)