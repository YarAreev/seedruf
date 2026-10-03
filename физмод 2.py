import numpy as np

class Source:
    def __init__(self):
        self.Y = 10000  # фотонов/МэВ
    
    def generate_photons(self, E):
        """
        Генерирует начальные направления фотонов для события с энергией E.
        
        Параметры:
        E (float): энергия события в МэВ
        
        Возвращает:
        list: список направлений фотонов в виде кортежей (x, y, z)
        """
        # Количество фотонов: линейная зависимость от энергии
        N = int(self.Y * E)
        
        directions = []
        for _ in range(N):
            # Генерируем углы для изотропного распределения
            cos_theta = np.random.uniform(-1, 1)  # cos(theta) равномерно на [-1, 1]
            sin_theta = np.sqrt(1 - cos_theta**2)  # sin(theta)
            phi = np.random.uniform(0, 2 * np.pi)  # phi равномерно на [0, 2π]
            
            # Декартовы координаты направления
            x = sin_theta * np.cos(phi)
            y = sin_theta * np.sin(phi)
            z = cos_theta
            
            directions.append((x, y, z))
        
        return directions
# Создаём источник
source = Source()

# Генерируем фотоны для события с энергией 2 МэВ
energy = 2.0  # МэВ
photon_directions = source.generate_photons(energy)

print(f"Энергия: {energy} МэВ")
print(f"Количество фотонов: {len(photon_directions)}")
print("Первые 5 направлений:")
for i, direction in enumerate(photon_directions[:5]):
    print(f"  Фотон {i+1}: ({direction[0]:.3f}, {direction[1]:.3f}, {direction[2]:.3f})")
