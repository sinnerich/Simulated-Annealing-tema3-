import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d


# Funcția Himmelblau
def f(x, y):
    return ((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2)


# Generarea graficului 3D al funcției
X = np.linspace(-6, 6, 100)
Y = np.linspace(-6, 6, 100)
x, y = np.meshgrid(X, Y)
F = f(x, y)

fig = plt.figure(figsize=(9, 9))
ax = plt.axes(projection='3d')
ax.contour3D(x, y, F, 450)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('F')
ax.set_title('Himmelblau Function')
ax.view_init(50, 50)
plt.show()

# Monitorizare optimizare
np.random.seed(42)  # Pentru reproductibilitate
num_iterations = 2000
best_values = []  # Lista pentru a stoca cele mai bune valori

# Inițializare aleatoare
current_x = np.random.uniform(-6, 6)
current_y = np.random.uniform(-6, 6)
best_value = f(current_x, current_y)

for i in range(1, num_iterations + 1):
    # Generare punct nou aleator în vecinătate
    new_x = current_x + np.random.uniform(-0.5, 0.5)
    new_y = current_y + np.random.uniform(-0.5, 0.5)
    new_value = f(new_x, new_y)

    # Dacă soluția e mai bună, o acceptăm
    if new_value < best_value:
        current_x, current_y = new_x, new_y
        best_value = new_value

    # Salvăm progresul la fiecare 200 de iterații
    if i % 200 == 0:
        best_values.append(best_value)
        print(f"Iterația {i}: Valoare cea mai bună = {best_value}")

# Grafic progres
plt.figure(figsize=(10, 6))
plt.plot(range(200, num_iterations + 1, 200), best_values, marker='o')
plt.title('Progresul valorii celei mai bune soluții')
plt.xlabel('Numărul de iterații')
plt.ylabel('Valoarea funcției')
plt.grid()
plt.show()
