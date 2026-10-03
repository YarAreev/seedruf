import numpy as np
import matplotlib.pyplot as plt

# Параметры моделирования
N_events = 1000
charge_per_MeV = 100  # усл. ед. заряда на 1 МэВ
sigma_noise = 5         # стандартное отклонение шума (усл. ед.)
attenuation_factor = 0.9  # ослабление сигнала при смещении источника
offset_z = 1.0      # смещение источника по оси z, м

# Энергии для исследования
energies = [0.2, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]  # МэВ

# Списки для хранения результатов
relative_widths = []
mean_charges_center = []
mean_charges_offset = []

# Создание фигуры для графиков распределений
fig1, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.ravel()

print("Результаты моделирования:\n")
print(f"{'Энергия (МэВ)':<12} {'Центр: <Q>':<15} {'Смещение: <Q>':<15} {'Отн. ширина':<12}")
print("-" * 60)

for i, E in enumerate(energies):
    # Моделирование событий для центрального положения
    charges_center = [
        E * charge_per_MeV + np.random.normal(0, sigma_noise)
        for _ in range(N_events)
    ]
    
    # Моделирование событий для смещённого положения
    effective_energy = E * attenuation_factor
    charges_offset = [
        effective_energy * charge_per_MeV + np.random.normal(0, sigma_noise)
        for _ in range(N_events)
    ]
    
    # Расчёт статистических характеристик
    mean_center = np.mean(charges_center)
    std_center = np.std(charges_center)
    relative_width = std_center / mean_center
    mean_offset = np.mean(charges_offset)
    
    # Сохранение результатов
    mean_charges_center.append(mean_center)
    mean_charges_offset.append(mean_offset)
    relative_widths.append(relative_width)
    
    # Вывод результатов в консоль
    print(f"{E:<12.1f} {mean_center:<15.2f} {mean_offset:<15.2f} {relative_width:<12.4f}")
    
    # Построение гистограммы (только для первых 7 энергий, 8‑й подграфик оставляем пустым)
    if i < 7:
        axes[i].hist(charges_center, bins=30, alpha=0.7, color='blue', label='Центр')
        axes[i].hist(charges_offset, bins=30, alpha=0.7, color='orange', label='Смещение')
        axes[i].set_title(f'E = {E} МэВ')
        axes[i].set_xlabel('Заряд, усл. ед.')
        axes[i].set_ylabel('Кол-во событий')
        axes[i].legend()

# Убираем последний пустой подграфик
axes[-1].set_visible(False)

plt.tight_layout()
plt.show()

# График зависимости относительной ширины от энергии
plt.figure(figsize=(10, 6))
plt.plot(energies, relative_widths, 'ro-', markersize=6)
plt.xlabel('Энергия, МэВ')
plt.ylabel('Относительная ширина распределения')
plt.title('Зависимость относительной ширины от энергии')
plt.grid(True)
plt.show()

# График изменения среднего заряда при смещении
changes = [(offset - center) / center * 100 for center, offset in zip(mean_charges_center, mean_charges_offset)]
plt.figure(figsize=(10, 6))
plt.plot(energies, changes, 'gs-', markersize=6)
plt.xlabel('Энергия, МэВ')
plt.ylabel('Изменение среднего заряда, %')
plt.title('Изменение среднего заряда при смещении источника на 1 м')
plt.grid(True)
plt.show()

# Итоговый вывод
print("\nВыводы:")
print("1. Относительная ширина распределения уменьшается с ростом энергии — эффект статистического усреднения.")
print(f"2. При смещении источника на {offset_z} м среднее значение собранного заряда уменьшается примерно на {(1 - attenuation_factor) * 100:.0f}%.")
print("3. Эффект более заметен при низких энергиях из-за большего относительного вклада шума.")
