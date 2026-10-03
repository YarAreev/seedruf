import numpy as np

class Photomultiplier:
    def __init__(self, mean_photoelectrons):
        self.a = mean_photoelectrons

    def generate_photoelectrons(self):
        return np.random.poisson(self.a)


class Detector:
    def __init__(self, radius, num_pmts, pmt_radius, a, Y):
        self.R = radius
        self.N = num_pmts
        self.r = pmt_radius
        self.a = a
        self.Y = Y

        # Создаём фотоумножители: равномерно распределяем по сфере
        self.pmts = [Photomultiplier(a) for _ in range(num_pmts)]
        self.pmt_centers = self._generate_pmt_positions()

    def _generate_pmt_positions(self):
        """
        Равномерно распределяет N точек на сфере радиуса R.
        Используем метод «равномерно по косинусу угла».
        """
        centers = []
        for _ in range(self.N):
            # Равномерное распределение по сфере
            theta = np.arccos(1 - 2 * np.random.rand())
            phi = 2 * np.pi * np.random.rand()
            x = self.R * np.sin(theta) * np.cos(phi)
            y = self.R * np.sin(theta) * np.sin(phi)
            z = self.R * np.cos(theta)
            centers.append(np.array([x, y, z]))
        return centers

    def simulate_event(self, energy_MeV):
        N_photons = int(energy_MeV * self.Y)
        total_charge = 0

        for _ in range(N_photons):
            x, y, z = 0.0, 0.0, 0.0  # источник в центре

            # Случайное направление (равномерно по сфере)
            theta = np.arccos(1 - 2 * np.random.rand())
            phi = 2 * np.pi * np.random.rand()
            nx = np.sin(theta) * np.cos(phi)
            ny = np.sin(theta) * np.sin(phi)
            nz = np.cos(theta)

            hit_pmt_index = self.find_hit_pmt(x, y, z, nx, ny, nz)
            if hit_pmt_index is not None:
                total_charge += self.pmts[hit_pmt_index].generate_photoelectrons()

        return total_charge

    def find_hit_pmt(self, x, y, z, nx, ny, nz):
        """
        Находит, в какой фотоумножитель попал луч.
        Возвращает индекс фотоумножителя или None.
        """
        # Решаем уравнение: (x + t*nx)^2 + (y + t*ny)^2 + (z + t*nz)^2 = R^2
        # Это квадратное уравнение: A*t^2 + B*t + C = 0
        A = nx**2 + ny**2 + nz**2  # = 1, если вектор единичный
        B = 2 * (x * nx + y * ny + z * nz)
        C = x**2 + y**2 + z**2 - self.R**2

        discriminant = B**2 - 4 * A * C
        if discriminant < 0:
            return None  # нет пересечения (не должно быть при старте из центра)

        sqrt_disc = np.sqrt(discriminant)
        t1 = (-B - sqrt_disc) / (2 * A)
        t2 = (-B + sqrt_disc) / (2 * A)

        # Выбираем положительный t (луч уходит наружу)
        ts = [t for t in [t1, t2] if t > 1e-9]
        if not ts:
            return None
        t_hit = min(ts)

        hit_x = x + nx * t_hit
        hit_y = y + ny * t_hit
        hit_z = z + nz * t_hit
        hit_point = np.array([hit_x, hit_y, hit_z])

        # Проверяем попадание в каждый фотоумножитель
        for i, center in enumerate(self.pmt_centers):
            dist = np.linalg.norm(hit_point - center)
            # На сфере расстояние по хорде: если оно меньше 2*r*sin(alpha/2), то попадает.
            # Для простоты считаем, что фотоумножитель — круг радиуса r на сфере.
            # Тогда условие попадания: расстояние по прямой <= r
            if dist <= self.r:
                return i

        return None

    def expected_charge(self):
        # Геометрический фактор: суммарная площадь фотоумножителей / площадь сферы
        # Площадь одного фотоумножителя ~ pi*r^2, площадь сферы = 4*pi*R^2
        # Но в твоей формуле уже заложена упрощённая версия: (N * r^2) / R^2
        return self.a * self.Y * (self.N * self.r**2 / self.R**2)


# Запуск моделирования
detector = Detector(radius=1.0, num_pmts=100, pmt_radius=0.1, a=5, Y=1000)
Q_sim = detector.simulate_event(energy_MeV=1)
Q_exp = detector.expected_charge()
print(f"Simulated charge: {Q_sim}")
print(f"Expected charge: {Q_exp}")
print(f"Deviation: {abs(Q_sim - Q_exp) / Q_exp * 100:.2f}%")

