"""
Лабораторная работа № 3. Вариант 6.
Быстрая сортировка (Хоар, опорный = первый) и восходящая сортировка слиянием.
Доп. задание Г6: трёхпутевое разбиение (Dutch flag).

Дисциплина: Основы алгоритмизации и программирование
Студент: Голдаева Валерия Валентиновна, группа БИ 2-1
"""
import random
import statistics
import time
import sys
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.setrecursionlimit(5000)


def generate_data(n, kind="random", lo=0, hi=100_000, seed=42):
    rng = random.Random(seed + n)
    if kind == "duplicates":
        return [rng.randint(0, 10) for _ in range(n)]
    data = [rng.randint(lo, hi) for _ in range(n)]
    if kind == "sorted":
        data.sort()
    elif kind == "reversed":
        data.sort(reverse=True)
    elif kind == "nearly_sorted":
        data.sort()
        for _ in range(max(1, n // 20)):
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
    return data


def measure(sort_func, data, repeats=3):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = sort_func(data)
        times.append(time.perf_counter() - start)
        assert result == sorted(data), f"{sort_func.__name__}: ошибка"
    return statistics.median(times)


def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def insertion_sort(arr):
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def quick_sort(arr):
    """Быстрая сортировка: разбиение Хоара, опорный = первый."""
    a = arr.copy()
    if len(a) > 1:
        _quick_sort(a, 0, len(a) - 1)
    return a


def _quick_sort(a, lo, hi):
    while lo < hi:
        p = _partition_hoare_first(a, lo, hi)
        if p - lo < hi - p:
            _quick_sort(a, lo, p)
            lo = p + 1
        else:
            _quick_sort(a, p + 1, hi)
            hi = p


def _partition_hoare_first(a, lo, hi):
    pivot = a[lo]
    i, j = lo - 1, hi + 1
    while True:
        i += 1
        while a[i] < pivot:
            i += 1
        j -= 1
        while a[j] > pivot:
            j -= 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def merge_sort(arr):
    """Восходящая (итеративная) сортировка слиянием."""
    a = arr.copy()
    n = len(a)
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left = a[i:i + width]
            right = a[i + width:i + 2 * width]
            merged = []
            li = rj = 0
            while li < len(left) and rj < len(right):
                if left[li] <= right[rj]:
                    merged.append(left[li]); li += 1
                else:
                    merged.append(right[rj]); rj += 1
            merged.extend(left[li:])
            merged.extend(right[rj:])
            a[i:i + 2 * width] = merged
        width *= 2
    return a


def quick_sort_3way(arr):
    """Трёхпутевое разбиение (Dutch National Flag), опорный = первый."""
    a = arr.copy()
    if len(a) > 1:
        _quick_3way(a, 0, len(a) - 1)
    return a


def _quick_3way(a, lo, hi):
    if lo >= hi:
        return
    lt, gt = lo, hi
    pivot = a[lo]
    i = lo
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    _quick_3way(a, lo, lt - 1)
    _quick_3way(a, gt + 1, hi)


def main():
    print("=" * 80)
    print("ЛАБОРАТОРНАЯ РАБОТА № 3 — ВАРИАНТ 6")
    print("Опорный: первый | Разбиение: Хоара | Слияние: восходящее | Доп: Г6")
    print("=" * 80)

    # Exp 1
    print("\nЭксперимент 1: четыре алгоритма")
    small = [500, 1000, 2000, 4000]
    algs1 = {"Пузырьком": bubble_sort, "Вставками": insertion_sort,
             "Быстрая": quick_sort, "Слиянием": merge_sort}
    res1 = {}
    print(f"{'n':>6}" + "".join(f"{n:>12}" for n in algs1))
    for n in small:
        data = generate_data(n)
        row = f"{n:>6}"
        res1[n] = {}
        for name, func in algs1.items():
            t = measure(func, data)
            res1[n][name] = t
            row += f"{t:>12.6f}"
        print(row)

    # Exp 2
    print("\nЭксперимент 2: большие размеры")
    large = [10_000, 20_000, 30_000, 40_000, 50_000]
    algs2 = {"Быстрая": quick_sort, "Слиянием": merge_sort, "sorted()": sorted}
    res2 = {}
    print(f"{'n':>8}" + "".join(f"{n:>12}" for n in algs2))
    for n in large:
        data = generate_data(n)
        row = f"{n:>8}"
        res2[n] = {}
        for name, func in algs2.items():
            t = measure(func, data)
            res2[n][name] = t
            row += f"{t:>12.6f}"
        print(row)

    # Exp 3
    print("\nЭксперимент 3: структура данных")
    for kind, n in [("random", 50000), ("sorted", 3000), ("reversed", 3000),
                    ("nearly_sorted", 50000), ("duplicates", 50000)]:
        data = generate_data(n, kind=kind)
        print(f"  {kind:>15} n={n}: быстрая {measure(quick_sort, data):.6f}, "
              f"слиянием {measure(merge_sort, data):.6f}")

    # G6
    print("\nГ6: 3-way vs классическая на D")
    for n in [10000, 20000, 50000]:
        data = generate_data(n, kind="duplicates")
        t1 = measure(quick_sort, data)
        t2 = measure(quick_sort_3way, data)
        print(f"  n={n}: классич. {t1:.6f}, 3-way {t2:.6f}, ускорение {t1/t2:.2f}x")

    # Plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for name in algs1:
        axes[0].plot(small, [res1[n][name] for n in small], marker="o", label=name)
    axes[0].set_yscale("log")
    axes[0].set_title("Эксперимент 1 (лог. шкала)")
    axes[0].set_xlabel("n"); axes[0].set_ylabel("Время, с")
    axes[0].legend(fontsize=8); axes[0].grid(True, alpha=0.3)

    for name in algs2:
        axes[1].plot(large, [res2[n][name] for n in large], marker="o", label=name)
    axes[1].set_title("Эксперимент 2")
    axes[1].set_xlabel("n"); axes[1].set_ylabel("Время, с")
    axes[1].legend(fontsize=8); axes[1].grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("lr3_plot.png", dpi=150)
    print("\nГрафик: lr3_plot.png")


if __name__ == "__main__":
    main()
