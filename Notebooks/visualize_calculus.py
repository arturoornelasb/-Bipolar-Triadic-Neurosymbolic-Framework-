import matplotlib.pyplot as plt
import numpy as np

def generate_plot():
    print("Generating convergence plot...")

    # --- 1. Replicate Experiment Data ---
    # Configuration identical to calculus_convergence_test.py
    acceleration = 2.0
    total_time = 4.0
    steps = 100
    dt = total_time / steps  # 0.04s

    # Data for the plot
    time_points = np.linspace(0, total_time, steps + 1)
    
    # A. Theoretical Curve (Continuous)
    # Analytical integral of v = 2t -> d = t^2
    theoretical_dist = time_points**2

    # B. Discrete Sum (Triadic UHRT)
    # Replicate cumulative sum of triads
    triadic_cumulative = [0.0]
    current_sum = 0.0
    
    for i in range(1, steps + 1):
        t_instant = i * dt
        v_instant = acceleration * t_instant
        
        # The microscopic triad: d_i = v_i * dt
        d_slice = v_instant * dt 
        
        current_sum += d_slice
        triadic_cumulative.append(current_sum)

    # --- 2. Academic Style Configuration ---
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plot Theoretical (Smooth Line)
    plt.plot(time_points, theoretical_dist, 
             color='#e74c3c', linewidth=2, linestyle='--', alpha=0.8,
             label=r'Theoretical Continuous ($d = t^2$)')

    # Plot Discrete (Stairs / Step Plot)
    # We use 'post' to show how the value is maintained during dt
    plt.step(time_points, triadic_cumulative, 
             color='#2980b9', linewidth=2, where='post',
             label=r'Discrete Triadic Sum ($\sum v \cdot dt$)')

    # --- 3. Anotaciones y Detalles ---
    
    # Highlight final error
    final_t = time_points[-1]
    final_theo = theoretical_dist[-1]  # 16.0
    final_triad = triadic_cumulative[-1] # 16.16
    
    plt.scatter([final_t], [final_triad], color='#2980b9', zorder=5)
    plt.scatter([final_t], [final_theo], color='#e74c3c', zorder=5)

    # Draw error line
    plt.plot([final_t, final_t], [final_theo, final_triad], color='black', linewidth=1)
    
    plt.annotate(fr'Discretization Error\n$\epsilon = {final_triad - final_theo:.2f}$',
                 xy=(final_t, (final_theo + final_triad)/2), 
                 xytext=(final_t - 1.5, final_theo - 2),
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

    # Labels
    plt.title('Emergence of Continuous Calculus from Discrete Arithmetic\n(N=100 Triads)', fontsize=14, fontweight='bold')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Accumulated Distance (m)', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    # Save
    filename = 'calculus_convergence_plot.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Plot saved successfully as: {filename}")

# Alias for notebook compatibility
visualize_convergence = generate_plot

if __name__ == "__main__":
    generate_plot()