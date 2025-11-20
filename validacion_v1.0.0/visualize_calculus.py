import matplotlib.pyplot as plt
import numpy as np

def generate_plot():
    print("Generando gráfica de convergencia...")

    # --- 1. Replicar los Datos del Experimento ---
    # Configuración idéntica a calculus_convergence_test.py
    acceleration = 2.0
    total_time = 4.0
    steps = 100
    dt = total_time / steps  # 0.04s

    # Datos para la gráfica
    time_points = np.linspace(0, total_time, steps + 1)
    
    # A. Curva Teórica (Continua)
    # Integral analítica de v = 2t -> d = t^2
    theoretical_dist = time_points**2

    # B. Suma Discreta (Triadas UHRT)
    # Replicamos la suma acumulativa de triadas
    triadic_cumulative = [0.0]
    current_sum = 0.0
    
    for i in range(1, steps + 1):
        t_instant = i * dt
        v_instant = acceleration * t_instant
        
        # La triada microscópica: d_i = v_i * dt
        d_slice = v_instant * dt 
        
        current_sum += d_slice
        triadic_cumulative.append(current_sum)

    # --- 2. Configuración de Estilo Académico ---
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plotear Teórico (Línea Suave)
    plt.plot(time_points, theoretical_dist, 
             color='#e74c3c', linewidth=2, linestyle='--', alpha=0.8,
             label=r'Continuo Teórico ($d = t^2$)')

    # Plotear Discreto (Escalera / Step Plot)
    # Usamos 'post' para mostrar cómo el valor se mantiene durante el dt
    plt.step(time_points, triadic_cumulative, 
             color='#2980b9', linewidth=2, where='post',
             label=r'Suma de Triadas Discretas ($\sum v \cdot dt$)')

    # --- 3. Anotaciones y Detalles ---
    
    # Resaltar el error final
    final_t = time_points[-1]
    final_theo = theoretical_dist[-1]  # 16.0
    final_triad = triadic_cumulative[-1] # 16.16
    
    plt.scatter([final_t], [final_triad], color='#2980b9', zorder=5)
    plt.scatter([final_t], [final_theo], color='#e74c3c', zorder=5)

    # Dibujar línea de error
    plt.plot([final_t, final_t], [final_theo, final_triad], color='black', linewidth=1)
    
    plt.annotate(f'Error de Discretización\n$\epsilon = {final_triad - final_theo:.2f}$',
                 xy=(final_t, (final_theo + final_triad)/2), 
                 xytext=(final_t - 1.5, final_theo - 2),
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

    # Etiquetas
    plt.title('Emergencia del Cálculo Continuo desde Aritmética Discreta\n(N=100 Triadas)', fontsize=14, fontweight='bold')
    plt.xlabel('Tiempo (s)', fontsize=12)
    plt.ylabel('Distancia Acumulada (m)', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    # Guardar
    filename = 'calculus_convergence_plot.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado exitosamente como: {filename}")

if __name__ == "__main__":
    generate_plot()