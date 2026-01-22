import numpy as np
import os
from GRASP import GRASPSolver
from preprocessing import apply_reductions
from metricas import calculate_metrics, report_statistics
from pathlib import Path

# Ejecutar Rum and Debug
# Ctrl + Shift + D
# Click en Run and Debug


# Funciones

# def load_matrix_robust(file_path):
#     matrix_data = []
#     with open(file_path, 'r') as f:
#         for line in f:
#             line = line.strip()
#             if not line: continue
#             clean_line = line.replace(" ", "").replace("\t", "")
#             if all(c in '01' for c in clean_line):
#                 matrix_data.append([int(c) for c in clean_line])
#     return np.array(matrix_data)

def load_matrix_robust(file_path):
    matrix_data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            clean_line = line.replace(" ", "").replace("\t", "")
            if all(c in '01' for c in clean_line):
                matrix_data.append([int(c) for c in clean_line])

    # Convierte a array y transpone (filas ↔ columnas)
    return np.array(matrix_data).T

# Metodos

def build_output_path(matrix_path, suffix="_reduced"):
    """
    Construye la ruta del archivo de salida agregando un sufijo al nombre original.
    
    :param matrix_path: Ruta del archivo de entrada.
    :param suffix: Sufijo a añadir al nombre del archivo.
    :return: Ruta del archivo de salida.
    """
    path = Path(matrix_path)
    return path.with_name(path.stem + suffix + path.suffix)

def save_matrix_txt(matrix, output_path):
    """
    Guarda una matriz NumPy en un archivo de texto.
    
    :param matrix: Matriz a guardar.
    :param output_path: Ruta del archivo de salida.
    """
    np.savetxt(output_path, matrix, fmt='%d')
    print(f"Matriz reducida guardada en: {output_path}")


def save_string_txt(text, output_path):
    """
    Guarda un string directamente en un archivo de texto.
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Texto guardado en: {output_path}")


# α = define el umbral de la RCL, determinando cuantos candidatos "buenos" entran a la selección aleatoria
# se coloca por defecto en 0.15 para que se tomen los RCL los test con ganancia alta
def run_experiment(matrix_path, mode='C', alpha=0.15):

    print(f"\n ** modo {mode} **")

    # Carga la matriz original desde disco.
    # Si la matriz está vacía o no es válida, se aborta el procesamiento.
    original_matrix = load_matrix_robust(matrix_path)
    if original_matrix.size == 0: 
        return

    # Obtiene el número original de casos de test (filas)
    # y de requisitos (columnas) de la matriz de entrada
    num_tests_orig, num_reqs_orig = original_matrix.shape
    
    # Aplica las reducciones sobre la matriz original y obtiene el mapeo de trazabilidad:
    # mapping[i] indica el índice del caso de test original correspondiente a la fila i
    # de la matriz reducida.
    reduced_matrix, mapping = apply_reductions(original_matrix, mode=mode)

    # Tamaños después del preprocesamiento
    num_tests_red, num_reqs_red = reduced_matrix.shape

    # Genera un resumen informativo de la matriz de cobertura, mostrando el número de
    # casos de prueba y requisitos antes y después del preprocesamiento aplicado.
    info_matriz = (
        f"\n--- INFORMACIÓN DE LA MATRIZ ---\n"
        f"Antes del preprocesamiento  -> Tests: {num_tests_orig} | Requerimientos: {num_reqs_orig}\n"
        f"Después del preprocesamiento-> Tests: {num_tests_red} | Requerimientos: {num_reqs_red}\n\n"
    )

    # Construye la ruta de salida incluyendo el modo de reducción y guarda la matriz resultante en un archivo .txt   
    output_path = build_output_path(matrix_path, f"_reduced_{mode}")
    save_matrix_txt(reduced_matrix, output_path)

    # Semillas
    seeds = [42, 123, 7, 99, 2024]
    results = []

    report = ""
    
    for seed in seeds:

        # Ejecuta una iteracíon de GRASP sobre la matriz reducida
        # Solution_indices_reduced = solución encontrada, exec_time = tiempo de ejecución
        solver = GRASPSolver(reduced_matrix, seed=seed)
        solution_indices_reduced, exec_time = solver.solve(alpha=alpha)

        # Traduce los índices obtenidos sobre la matriz reducida
        # a los índices reales de la matriz original, utilizando
        # el vector de trazabilidad generado durante la reducción
        solution_indices_original = mapping[list(solution_indices_reduced)]
        
        # Convierte los índices internos (base 0) a los IDs reales de los tests (base 1),
        # tal como aparecen en el archivo original
        tests_seleccionados = [int(i + 1) for i in solution_indices_original]
        
        # Encabezado de la semilla
        report += f"Semilla {seed}: S = {sorted(tests_seleccionados)}\n\n"
        print(f"\nSemilla {seed}: S = {sorted(tests_seleccionados)}")

        # Detalle usando la matriz ORIGINAL para ver todos los bits y requisitos
        for idx_orig in solution_indices_original:
            fila = original_matrix[idx_orig]
            reqs = np.where(fila == 1)[0] + 1
            report += f"  - Test {idx_orig + 1} cubre: {reqs.tolist()}\n"
            print(f"  - Test {idx_orig + 1} cubre: {reqs.tolist()}")

        # Separación entre semillas
        report += "\n"
        
        # CÁLCULO DE MÉTRICAS CON LOS ÍNDICES REALES
        tssr, fdcloss = calculate_metrics(num_tests_orig, len(solution_indices_original), 
                                         original_matrix, solution_indices_original)
        
        results.append({'tssr': tssr, 'fdcloss': fdcloss, 'time': exec_time, 'size': len(solution_indices_original)})

    report += info_matriz
    report += report_statistics(results)

    # Construye la ruta de salida incluyendo el modo de reducción y guarda la matriz resultante en un archivo .txt   
    output_path = build_output_path(matrix_path, f"_Output_{mode}")
    save_string_txt(report, output_path)


 # ** Implementación main ***

def main():

    # Lista de archivos de matrices a procesar.
    # Descomenta o añade rutas según los experimentos que quieras ejecutar.
    matrix_files = [
        "matrices/matrix_7_60_1.txt",
        "matrices/matrix_18_213_1.txt",
        "matrices/matrix_33_890_1.txt",
        "matrices/matrix_36_508_1.txt",
        "matrices/matrix_94_3647_1.txt",
    ]

    # Modos de ejecución del experimento
    # Commenta los modos a no implementar
    modes = (
        "A",
        "B",
        "C"
        )

    # Ejecuta el experimento para cada combinación de matriz y modo
    for matrix_path in matrix_files:
        for mode in modes:
            run_experiment(matrix_path, mode)


# **** Ejecución segura ****

if __name__ == "__main__":
    main()