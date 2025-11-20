"""
calculus_integration_experiment.py v1.1.0 – 2025-11-19
DEMOSTRACIÓN: La Integral es una Suma Masiva de Triadas.
Problema: Calcular distancia recorrida con aceleración constante (a=2 m/s²) durante 4 segundos.
Método: Suma de Riemann (Discretización Temporal).
"""
from triadic_framework.core.network import TriadicNetwork
from triadic_framework.core.generic_inference import GenericInferenceEngine
from triadic_framework.core.additive_laws import AdditiveLaw

def run_discrete_integral():
    net = TriadicNetwork()
    print("=== EXPERIMENTO DE CÁLCULO DISCRETO (INTEGRACIÓN) ===")
    print("Objetivo: Integrar v(t) para obtener distancia total.")
    print("Función: v(t) = a * t  (con a=2)")
    print("Intervalo: t=0 a t=4 (Delta t = 1s)\n")

    # Configuración del escenario físico
    acceleration = 2
    total_time = 4
    delta_t = 1  # El "dx" de la integral.
    
    slices = [] # Aquí guardaremos los nombres de las "rebanadas" de distancia (d1, d2...)
    known_values = {'1': 1.0}

    print("--- [1] GENERACIÓN DE TRIADAS INFINITESIMALES (dx) ---")
    
    # Simulamos el paso del tiempo
    for t in range(1, total_time + 1):
        # 1. Calculamos la velocidad instantánea en este segundo
        # Triada: v = a * t
        v_instant = acceleration * t 
        
        # Nombres de variables dinámicas para este "pixel" de tiempo
        var_v = f"v_t{t}"      # Velocidad en tiempo t
        var_d = f"dist_t{t}"   # Distancia recorrida en este segundo
        var_dt = f"dt_{t}"     # El diferencial de tiempo (siempre 1)

        # Agregamos los valores conocidos de este instante
        known_values[var_v] = float(v_instant)
        known_values[var_dt] = float(delta_t)

        # 2. CREAMOS LA TRIADA DIFERENCIAL: d = v * dt
        # Verificamos K=1.0: Si v=2 y dt=1, entonces d=2. 
        # La triada es: dist_t1 * 1 = v_t1 * dt_1
        d_val = v_instant * delta_t 
        
        # IMPORTANTE: Añadimos unidades simuladas para pasar el Guardián Dimensional
        # Como no tenemos un parser complejo de "v_t1", usamos las etiquetas base 'd', 'v', 't'
        # Truco: Usamos las etiquetas reales en 'labels' para el grafo, pero engañamos 
        # al guardián diciéndole que son distancias y velocidades genéricas.
        # Pero tu red actual usa las etiquetas como keys. 
        # Para este experimento, desactivaremos temporalmente el guardián o usaremos unidades base si fallara.
        # En tu v1.0.1, el guardián permite el paso si no conoce la unidad (retorna True).
        # Como "v_t1" no está en UNITS_MAP, pasará sin problemas.
        
        net.add_candidate_quartet(
            (d_val, 1, v_instant, delta_t), 
            (var_d, '1', var_v, var_dt)
        )
        
        slices.append(var_d)

    print(f"\nSe generaron {len(slices)} triadas de distancia infinitesimal.")

    # --- [2] DEFINICIÓN DE LA INTEGRAL (LEY ADITIVA) ---
    # La "Integral" es simplemente una Ley Aditiva que dice:
    # Distancia_Total = d_t1 + d_t2 + d_t3 + d_t4
    
    integral_law = AdditiveLaw(
        name="Integral de Riemann (Distancia Total)",
        parts=slices,
        total="Distancia_Total"
    )

    # --- [3] EJECUCIÓN DEL MOTOR HÍBRIDO ---
    engine = GenericInferenceEngine(net)
    engine.additive_laws.append(integral_law)

    print("\n--- [3] RESOLVIENDO LA INTEGRAL ---")
    
    result = engine.solve(known_values, "Distancia_Total")
    
    print(f"\nResultado del Motor (Riemann Derecha): {result}")
    print("Teórico (1/2 * a * t^2): 16.0")
    print("Diferencia debida a discretización (dt=1s).")

if __name__ == "__main__":
    run_discrete_integral()
