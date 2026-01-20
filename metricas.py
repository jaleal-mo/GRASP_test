import numpy as np

def calculate_metrics(T_count, S_count, matrix, S_indices):
    # TSSR = 1 - (|S| / |T|)
    tssr = 1 - (S_count / T_count)
    
    # FDCLOSS basado en cobertura
    # U(T) son los requisitos cubiertos por la suite original
    u_t = np.sum(np.any(matrix, axis=0)) 
    # U(S) son los requisitos cubiertos por el subconjunto S
    u_s = np.sum(np.any(matrix[S_indices], axis=0))
    
    fdcloss = 1 - (u_s / u_t) if u_t > 0 else 0
    return tssr, fdcloss

import numpy as np

def report_statistics(results):
    tssr_vals = [r['tssr'] for r in results]
    fdcloss_vals = [r['fdcloss'] for r in results]
    times = [r['time'] for r in results]
    sizes = [r['size'] for r in results]
    
    print(f"\n--- ESTADÍSTICOS FINALES (5 Semillas) ---")
    print(f"TSSR    -> Media: {np.mean(tssr_vals):.4f} | Min: {np.min(tssr_vals):.4f} | Max: {np.max(tssr_vals):.4f} | Std: {np.std(tssr_vals):.4f}")
    print(f"FDCLOSS -> Media: {np.mean(fdcloss_vals):.4f} (Objetivo: 0.0000)")
    print(f"Tamaño S-> Media: {np.mean(sizes):.1f} tests")
    print(f"Tiempo  -> Media: {np.mean(times):.6f}s")