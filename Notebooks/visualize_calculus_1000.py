import matplotlib.pyplot as plt
import numpy as np

def generate_plot():
    print("Generating High Resolution Plot (N=1000)...")

    # --- 1. High Resolution Setup ---
    acceleration = 2.0
    total_time = 4.0
    steps = 1000  # <--- INCREASED RESOLUTION (Was 100)
    dt = total_time / steps  # dt = 0.004s

    # Data for plot
    time_points = np.linspace(0, total_time, steps + 1)
    
    # A. Theoretical Curve (Continuous)
    theoretical_dist = time_points**2

    # B. Discrete Sum (Triadic UHRT)
    triadic_cumulative = [0.0]
    current_sum = 0.0
    
    for i in range(1, steps + 1):
        t_instant = i * dt
        v_instant = acceleration * t_instant
        d_slice = v_instant * dt 
        current_sum += d_slice
        triadic_cumulative.append(current_sum)

    # --- 2. Visual Setup ---
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plot Theoretical
    plt.plot(time_points, theoretical_dist, 
             color='#e74c3c', linewidth=2.5, linestyle='-', alpha=0.6,
             label=r'Theoretical Continuous ($d = t^2$)')

    # Plot Discrete
    plt.step(time_points, triadic_cumulative, 
             color='#2980b9', linewidth=1.5, where='post',
             label=fr'Triadic Sum ($N={steps}$)')

    # --- 3. Zoom to Error (Microscopic) ---
    final_t = time_points[-1]
    final_theo = theoretical_dist[-1]  # 16.0
    final_triad = triadic_cumulative[-1] # 16.016 (Theoretical)
    
    # End points
    plt.scatter([final_t], [final_triad], color='#2980b9', s=30, zorder=5)
    plt.scatter([final_t], [final_theo], color='#e74c3c', s=30, zorder=5)

    # Calculate Error
    error = final_triad - final_theo
    
    # Note: Zoom visual annotation
    plt.annotate(f'Successful Convergence\nError: {error:.4f}\n(10x smaller than N=100)',
                 xy=(final_t, final_triad), 
                 xytext=(final_t - 1.8, final_theo - 3),
                 arrowprops=dict(arrowstyle='->', color='black'),
                 fontsize=11, 
                 bbox=dict(boxstyle="round,pad=0.3", fc="#e8f6f3", ec="#1abc9c", alpha=1.0))

    plt.title(f'Discrete Calculus Convergence: High Resolution\n(N={steps} steps, dt={dt:.3f}s)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Accumulated Distance (m)', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    filename = 'calculus_convergence_high_res.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ High precision plot saved: {filename}")
    print(f"   Final calculated error: {error:.5f}")

# Alias
visualize_convergence_1000 = generate_plot

if __name__ == "__main__":
    generate_plot()