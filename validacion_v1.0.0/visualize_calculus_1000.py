import matplotlib.pyplot as plt
import numpy as np

def generate_plot():
    print("Generando gráfica de Alta Resolución (N=1000)...")

    # --- 1. Configuración de Alta Resolución ---
    acceleration = 2.0
    total_time = 4.0
    steps = 1000  # <--- AUMENTO DE RESOLUCIÓN (Antes 100)
    dt = total_time / steps  # dt = 0.004s

    # Datos para la gráfica
    time_points = np.linspace(0, total_time, steps + 1)
    
    # A. Curva Teórica (Continua)
    theoretical_dist = time_points**2

    # B. Suma Discreta (Triadas UHRT)
    triadic_cumulative = [0.0]
    current_sum = 0.0
    
    for i in range(1, steps + 1):
        t_instant = i * dt
        v_instant = acceleration * t_instant
        d_slice = v_instant * dt 
        current_sum += d_slice
        triadic_cumulative.append(current_sum)

    # --- 2. Configuración Visual ---
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plotear Teórico
    plt.plot(time_points, theoretical_dist, 
             color='#e74c3c', linewidth=2.5, linestyle='-', alpha=0.6,
             label=r'Continuo Teórico ($d = t^2$)')

    # Plotear Discreto (Ahora parece casi una curva suave por la alta densidad)
    plt.step(time_points, triadic_cumulative, 
             color='#2980b9', linewidth=1.5, where='post',
             label=fr'Suma de Triadas ($N={steps}$)')

    # --- 3. Zoom al Error (Microscópico) ---
    final_t = time_points[-1]
    final_theo = theoretical_dist[-1]  # 16.0
    final_triad = triadic_cumulative[-1] # 16.016 (Teórico)
    
    # Puntos finales
    plt.scatter([final_t], [final_triad], color='#2980b9', s=30, zorder=5)
    plt.scatter([final_t], [final_theo], color='#e74c3c', s=30, zorder=5)

    # Error calculado
    error = final_triad - final_theo
    
    # Nota: Como el error es tan pequeño, hacemos zoom visual en la anotación
    plt.annotate(f'Convergencia Exitosa\nError: {error:.4f}\n(10x menor que con N=100)',
                 xy=(final_t, final_triad), 
                 xytext=(final_t - 1.8, final_theo - 3),
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=11, 
                 bbox=dict(boxstyle="round,pad=0.3", fc="#e8f6f3", ec="#1abc9c", alpha=1.0))

    plt.title(f'Convergencia del Cálculo Discreto: Alta Resolución\n(N={steps} pasos, dt={dt:.3f}s)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Distancia Acumulada (m)', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    filename = 'calculus_convergence_high_res.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico de alta precisión guardado: {filename}")
    print(f"   Error final calculado: {error:.5f}")

if __name__ == "__main__":
    generate_plot()