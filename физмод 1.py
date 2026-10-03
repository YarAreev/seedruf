import numpy as np

class Detector:
    def __init__(self):
        self.R = 2  # радиус детектора, м
        self.N = 40  # количество фотоумножителей
        self.r = 0.1  # радиус фотоумножителя, м (10 см = 0.1 м)
        self.a = 0.5  # дополнительный параметр
        self.photomultiplier_coords = []  # список для хранения координат

    def place_photomultipliers(self):
        indices = np.arange(0, self.N, dtype=float) + 0.5
        phi = np.arccos(1 - 2 * indices / self.N)
        theta = np.pi * (1 + np.sqrt(5)) * indices

        x = self.R * np.sin(phi) * np.cos(theta)
        y = self.R * np.sin(phi) * np.sin(theta)
        z = self.R * np.cos(phi)

        self.photomultiplier_coords = np.column_stack((x, y, z))

    def is_point_covered(self, point):
        """
        Проверяет, принадлежит ли точка какому‑либо фотоумножителю.
        point: кортеж (x, y, z) — координаты точки.
        Возвращает: True, если точка покрыта, иначе False.
        """
        point = np.array(point)
        for pm_coord in self.photomultiplier_coords:
            distance = np.linalg.norm(point - pm_coord)
            if distance <= self.r:
                return True
        return False

# Создаём детектор
detector = Detector()

# Размещаем фотоумножители
detector.place_photomultipliers()

# Проверяем точки
test_point_1 = (1, 1, 1)  # точка внутри сферы
test_point_2 = (3, 0, 0)  # точка вне сферы

print(f"Точка {test_point_1} покрыта: {detector.is_point_covered(test_point_1)}")
print(f"Точка {test_point_2} покрыта: {detector.is_point_covered(test_point_2)}")

# Выводим координаты фотоумножителей
print("Координаты фотоумножителей:")
for i, coord in enumerate(detector.photomultiplier_coords):
    print(f"  PM {i+1}: ({coord[0]:.3f}, {coord[1]:.3f}, {coord[2]:.3f})")
