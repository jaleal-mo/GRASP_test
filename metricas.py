import numpy as np

# --- Ejemplo de cálculo de métricas obligatorias ---
def calculate_metrics(original_size, selected_size, matrix, selected_indices):
    """
    Calcula las métricas obligatorias de evaluación del proceso de
    minimización de la suite de pruebas.

    Las métricas calculadas son:
    - TSSR (Test Suite Size Reduction): mide la proporción de reducción
      del tamaño de la suite de pruebas respecto a la original.
    - FDCLOSS (Fault Detection Capability Loss): aproxima la pérdida de
      capacidad de detección de fallos mediante la pérdida de cobertura
      total de requisitos.

    Parámetros:
    - original_size (int): número total de tests en la suite original |T|.
    - selected_size (int): número de tests seleccionados en la solución |S|.
    - matrix (np.ndarray): matriz binaria de cobertura test–requisito.
    - selected_indices (list[int]): índices de los tests seleccionados.

    Retorna:
    - tuple(float, float): valores de TSSR y FDCLOSS respectivamente.
    """

    # TSSR (Test Suite Size Reduction):
    # Mide la proporción de reducción del tamaño de la suite de pruebas.
    # TSSR = 1 − (|S| / |T|)
    tssr = 1 - (selected_size / original_size)

    # FDCLOSS (Fault Detection Capability Loss):
    # Aproxima la pérdida de capacidad de detección de fallos usando la
    # cobertura total de requisitos (no se dispone de fallos reales).
    
    # U(T): número de requisitos cubiertos por la suite original
    u_t = np.sum(np.any(matrix, axis=0)) # Requisitos cubiertos por T

    # U(S): número de requisitos cubiertos por la suite reducida
    u_s = np.sum(np.any(matrix[selected_indices], axis=0)) # Requisitos cubiertos por S

    # FDCLOSS = 1 − (|U(S)| / |U(T)|)
    fdcloss = 1 - (u_s / u_t) if u_t > 0 else 0
    
    # Retorna ambas métricas de evaluación
    return tssr, fdcloss

def report_statistics(results):
    """
    Genera un reporte estadístico agregado a partir de múltiples ejecuciones
    independientes del algoritmo de reducción de la suite de pruebas.

    La función analiza los resultados obtenidos en varias ejecuciones
    (por ejemplo, con diferentes semillas aleatorias) y calcula
    estadísticas descriptivas sobre las métricas de evaluación y
    el rendimiento computacional.

    En particular, se reportan:
    - TSSR (Test Suite Size Reduction): se calcula la media, el valor mínimo,
      el valor máximo y la desviación estándar, con el fin de evaluar
      el grado de reducción alcanzado y la estabilidad del algoritmo.
    - FDCLOSS (Fault Detection Capability Loss): se reporta el valor medio,
      comparándolo con el objetivo ideal de pérdida nula de cobertura.
    - Tamaño de la suite reducida: número medio de tests seleccionados.
    - Tiempo de ejecución: tiempo medio requerido por el algoritmo.

    Parámetros:
    - results (list[dict]): lista de resultados de cada ejecución, donde
      cada diccionario contiene las métricas calculadas (TSSR, FDCLOSS),
      el tamaño de la solución, y el tiempo de ejecución.

    Retorna:
    - None: la función imprime en pantalla el resumen estadístico final.
    """

    # Extrae los valores de TSSR obtenidos en cada ejecución
    # para analizar el grado de reducción alcanzado por el algoritmo
    tssr_vals = [r['tssr'] for r in results]

    # Extrae los valores de FDCLOSS de cada ejecución
    # con el fin de evaluar la pérdida de cobertura asociada a la reducción
    fdcloss_vals = [r['fdcloss'] for r in results]

    # Extrae los tiempos de ejecución de cada corrida
    # para medir el rendimiento computacional del algoritmo
    times = [r['time'] for r in results]

    # Extrae el tamaño de la suite reducida en cada ejecución
    # es decir, el número de tests seleccionados en la solución final
    sizes = [r['size'] for r in results]
    
    print(f"\n--- ESTADÍSTICOS FINALES (5 Semillas) ---")
    print(f"TSSR    -> Media: {np.mean(tssr_vals):.4f} | Min: {np.min(tssr_vals):.4f} | Max: {np.max(tssr_vals):.4f} | Std: {np.std(tssr_vals):.4f}")
    print(f"FDCLOSS -> Media: {np.mean(fdcloss_vals):.4f} (Objetivo: 0.0000)")
    print(f"Tamaño S-> Media: {np.mean(sizes):.1f} tests")
    print(f"Tiempo  -> Media: {np.mean(times):.6f}s")