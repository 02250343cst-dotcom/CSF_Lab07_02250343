# Task 1: Bubble Sort

def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

lst = [64, 34, 25, 12, 22, 11, 90]
print("Original List:", lst)
print("Sorted List:  ", bubble_sort(lst))