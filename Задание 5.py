def minimum_total(triangle):
    """
    Находит минимальную сумму пути от вершины до основания треугольника.
    
    Args:
        triangle: List[List[int]] - треугольник в виде списка списков
    
    Returns:
        int - минимальная сумма пути
    """
    if not triangle:
        return 0
    
    n = len(triangle)
    
    # Начинаем с предпоследней строки и идём вверх
    for i in range(n-2, -1, -1):
        for j in range(len(triangle[i])):
            # Для каждого элемента выбираем минимальный путь из двух возможных ниже
            triangle[i][j] += min(triangle[i+1][j], triangle[i+1][j+1])
    
    return triangle[0][0]

def get_min_path(triangle):
    """
    Восстанавливает сам путь с минимальной суммой.
    
    Args:
        triangle: List[List[int]] - исходный треугольник
    
    Returns:
        tuple: (минимальная_сумма, путь)
    """
    if not triangle:
        return 0, []
    
    # Создаем копию для восстановления пути
    import copy
    triangle_copy = copy.deepcopy(triangle)
    n = len(triangle_copy)
    
    # Вычисляем минимальные суммы
    for i in range(n-2, -1, -1):
        for j in range(len(triangle_copy[i])):
            triangle_copy[i][j] += min(triangle_copy[i+1][j], triangle_copy[i+1][j+1])
    
    # Восстанавливаем путь
    path = []
    j = 0  # начинаем с вершины
    
    for i in range(n):
        path.append(triangle[i][j])
        # Если не последняя строка, выбираем следующий индекс
        if i < n-1:
            if triangle_copy[i+1][j] < triangle_copy[i+1][j+1]:
                j = j  # остаемся на том же индексе
            else:
                j = j + 1  # переходим на следующий индекс
    
    return triangle_copy[0][0], path

# Тесты из условия
if __name__ == "__main__":
    # Тест 1
    triangle1 = [
        [2],
        [3, 4],
        [6, 5, 7],
        [4, 1, 8, 3]
    ]
    
    min_sum1, path1 = get_min_path(triangle1)
    print(f"Тест 1:")
    print(f"Минимальный путь: {' → '.join(map(str, path1))}")
    print(f"Результат: {min_sum1}")
    print()
    
    # Тест 2
    triangle2 = [
        [-1],
        [2, 3],
        [1, -1, -3],
        [4, 2, 1, 3]
    ]
    
    min_sum2, path2 = get_min_path(triangle2)
    print(f"Тест 2:")
    print(f"Минимальный путь: {' → '.join(map(str, path2))}")
    print(f"Результат: {min_sum2}")