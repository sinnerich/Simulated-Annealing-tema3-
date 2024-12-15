import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

# Funcția Himmelblau
def f(x, y):
    return ((x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2)

# Parametrii pentru exemple
examples = [
    {"temp_init": 100, "cooling_rate": 0.9, "temp_min": 0.1, "num_iterations": 2000},
    {"temp_init": 50, "cooling_rate": 0.95, "temp_min": 0.01, "num_iterations": 1500},
    {"temp_init": 200, "cooling_rate": 0.8, "temp_min": 1, "num_iterations": 2500},
]

# Generarea graficului 3D al funcției
X = np.linspace(-6, 6, 100)
Y = np.linspace(-6, 6, 100)
x, y = np.meshgrid(X, Y)
F = f(x, y)

# Vizualizare funcție Himmelblau
fig = plt.figure(figsize=(9, 9))
ax = plt.axes(projection='3d')
ax.contour3D(x, y, F, 450)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('F')
ax.set_title('Himmelblau Function')
ax.view_init(50, 50)
plt.show()

# Funcție de optimizare folosind Simulated Annealing
def simulated_annealing(params):
    np.random.seed(42)  # Pentru reproductibilitate
    temp = params["temp_init"]
    cooling_rate = params["cooling_rate"]
    temp_min = params["temp_min"]
    num_iterations = params["num_iterations"]

    current_x = np.random.uniform(-6, 6)
    current_y = np.random.uniform(-6, 6)
    best_x, best_y = current_x, current_y
    best_value = f(current_x, current_y)

    trajectory = [(current_x, current_y)]

    for i in range(num_iterations):
        new_x = current_x + np.random.uniform(-0.5, 0.5)
        new_y = current_y + np.random.uniform(-0.5, 0.5)
        new_value = f(new_x, new_y)

        # Acceptăm noua soluție cu probabilitate dependentă de temperatură
        delta = new_value - f(current_x, current_y)
        if delta < 0 or np.random.rand() < np.exp(-delta / temp):
            current_x, current_y = new_x, new_y
            if new_value < best_value:
                best_x, best_y = new_x, new_y
                best_value = new_value

        # Scădem temperatura
        temp *= cooling_rate
        trajectory.append((current_x, current_y))

        # Oprire dacă temperatura scade sub minim
        if temp < temp_min:
            break

    return trajectory, best_value

# Rulare pentru fiecare set de parametri
final_trajectories = []
final_best_values = []

for idx, params in enumerate(examples):
    trajectory, best_value = simulated_annealing(params)
    final_trajectories.append(trajectory)
    final_best_values.append(best_value)

    # Grafic individual pentru fiecare exemplu
    fig, ax = plt.subplots(figsize=(10, 10))
    contour = ax.contour(X, Y, F, levels=50, cmap='viridis')
    ax.clabel(contour, inline=True, fontsize=8)
    ax.set_title(
        f"Traiectorie - Ex. {idx + 1}: Temp. Inițială={params['temp_init']}, "
        f"Rata Răcire={params['cooling_rate']}, Temp. Min={params['temp_min']}"
    )
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    trajectory = np.array(trajectory)
    ax.plot(trajectory[:, 0], trajectory[:, 1], marker='o', label='Traiectorie', color='blue')
    # Modificare pentru punctul final
    ax.scatter(
        trajectory[-1, 0], trajectory[-1, 1],
        color='red', s=150, zorder=5, label='Minim final', edgecolor='black', linewidth=1.5
    )
    ax.annotate(
        f"({trajectory[-1, 0]:.2f}, {trajectory[-1, 1]:.2f})",
        (trajectory[-1, 0], trajectory[-1, 1]),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=10,
        color='red',
        fontweight='bold'
    )
    ax.legend()
    plt.savefig(f"example_{idx + 1}.png")
    plt.show()

# Grafic comparativ
fig, ax = plt.subplots(figsize=(10, 10))
contour = ax.contour(X, Y, F, levels=50, cmap='viridis')
ax.clabel(contour, inline=True, fontsize=8)
ax.set_title('Traiectorii finale pentru toate exemplele')
ax.set_xlabel('X')
ax.set_ylabel('Y')

colors = ['blue', 'green', 'orange']
for idx, trajectory in enumerate(final_trajectories):
    trajectory = np.array(trajectory)
    ax.plot(trajectory[:, 0], trajectory[:, 1], marker='o', label=f'Exemplu {idx + 1}', color=colors[idx])
    ax.scatter(trajectory[-1, 0], trajectory[-1, 1], color='red', s=150, zorder=5, label=f'Final Ex. {idx + 1}')

plt.legend()
plt.grid()
plt.savefig("all_trajectories.png")
plt.show()
