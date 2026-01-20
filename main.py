import numpy as np
import os
from GRASP import GRASPSolver
from preprocessing import apply_reductions
from metricas import calculate_metrics, report_statistics

def load_matrix_robust(file_path):
    matrix_data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            clean_line = line.replace(" ", "").replace("\t", "")
            if all(c in '01' for c in clean_line):
                matrix_data.append([int(c) for c in clean_line])
    return np.array(matrix_data)


def run_experiment(matrix_path, mode='C', alpha=0.15):
    original_matrix = load_matrix_robust(matrix_path)
    if original_matrix.size == 0: return

    num_tests_orig, num_reqs_orig = original_matrix.shape
    
    # OBTENEMOS EL MAPEO: mapping[idx_reducido] = idx_original
    reduced_matrix, mapping = apply_reductions(original_matrix, mode=mode)
    
    seeds = [42, 123, 7, 99, 2024]
    results = []
    
    for seed in seeds:
        solver = GRASPSolver(reduced_matrix, seed=seed)
        solution_indices_reduced, exec_time = solver.solve(alpha=alpha)

        # TRADUCCIÓN CRÍTICA: Convertimos índices del solver a índices originales
        solution_indices_original = mapping[list(solution_indices_reduced)]
        
        # Ahora sí, el ID es el real del archivo original
        tests_seleccionados = [int(i + 1) for i in solution_indices_original]
        
        print(f"\nSemilla {seed}: S = {sorted(tests_seleccionados)}")

        # Detalle usando la matriz ORIGINAL para ver todos los bits y requisitos
        for idx_orig in solution_indices_original:
            fila = original_matrix[idx_orig]
            reqs = np.where(fila == 1)[0] + 1
            print(f"  - Test {idx_orig + 1} cubre: {reqs.tolist()}")
        
        # CÁLCULO DE MÉTRICAS CON LOS ÍNDICES REALES
        tssr, fdcloss = calculate_metrics(num_tests_orig, len(solution_indices_original), 
                                         original_matrix, solution_indices_original)
        
        results.append({'tssr': tssr, 'fdcloss': fdcloss, 'time': exec_time, 'size': len(solution_indices_original)})

    report_statistics(results)

if __name__ == "__main__":
    # Ejecución de ejemplo
    #  print("\n ** modo A **")
    #  run_experiment("matrices/matrix_7_60_1.txt", mode='A')
    #  print("\n ** modo B **")
    #  run_experiment("matrices/matrix_7_60_1.txt", mode='B')
    #  print("\n ** modo C **")
    #  run_experiment("matrices/matrix_7_60_1.txt", mode='C')

    # run_experiment("matrices/matrix_18_213_1.txt", mode='A')
    # run_experiment("matrices/matrix_18_213_1.txt", mode='B')
    # run_experiment("matrices/matrix_18_213_1.txt", mode='C')

    # run_experiment("matrices/matrix_33_890_1.txt", mode='A')
    # run_experiment("matrices/matrix_33_890_1.txt", mode='B')
    # run_experiment("matrices/matrix_33_890_1.txt", mode='C')

    # run_experiment("matrices/matrix_36_508_1.txt", mode='A')
    # run_experiment("matrices/matrix_36_508_1.txt", mode='B')
    # run_experiment("matrices/matrix_36_508_1.txt", mode='C')

    # run_experiment("matrices/matrix_94_3647_1.txt", mode='A')
    # run_experiment("matrices/matrix_94_3647_1.txt", mode='B')
     print("\n ** modo C **")
     run_experiment("matrices/matrix_94_3647_1.txt", mode='C')