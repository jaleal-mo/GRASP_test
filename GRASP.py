import numpy as np
import random
import time

class GRASPSolver:
    def __init__(self, matrix, seed):
        self.matrix = matrix  # Filas = Tests, Columnas = Requisitos
        self.num_tests, self.num_reqs = matrix.shape
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)

    def solve(self, alpha=0.1):
        start_time = time.time()
        
        # 1. Fase Constructiva Aleatorizada 
        solution = self._constructive_phase(alpha)
        
        # 2. Fase de Mejora (Búsqueda Local) 
        solution = self._local_search(solution)
        
        execution_time = time.time() - start_time
        return solution, execution_time

    def _constructive_phase(self, alpha):
        solution = set()
        covered_reqs = np.zeros(self.num_reqs, dtype=bool)
        # Solo intentamos cubrir los requisitos que son cubribles
        target_reqs = np.any(self.matrix, axis=0) 
        
        while not np.all(covered_reqs[target_reqs]):
            # Calcular ganancia marginal de cada test no seleccionado
            uncovered_idx = np.where(~covered_reqs & target_reqs)[0]
            gains = np.sum(self.matrix[:, uncovered_idx], axis=1)
            
            max_g = np.max(gains)
            min_g = np.min(gains[gains > 0]) if np.any(gains > 0) else 0
            
            # Umbral para la Lista Restringida de Candidatos (RCL) 
            threshold = max_g - alpha * (max_g - min_g)
            rcl = np.where(gains >= threshold)[0]
            
            # Selección aleatoria de la RCL 
            selected_test = random.choice(rcl)
            solution.add(selected_test)
            
            # Actualizar cobertura
            covered_reqs |= self.matrix[selected_test].astype(bool)
            
        return list(solution)

    def _local_search(self, solution):
        # Intenta eliminar tests redundantes para minimizar el tamaño S
        improved_solution = sorted(solution, key=lambda x: np.sum(self.matrix[x]), reverse=False)
        final_s = set(improved_solution)
        
        for test in improved_solution:
            # Si quitamos el test, ¿seguimos cubriendo todo?
            temp_solution = final_s - {test}
            if self._check_full_coverage(temp_solution):
                final_s = temp_solution
                
        return list(final_s)

    def _check_full_coverage(self, test_indices):
        if not test_indices: return False
        combined_coverage = np.any(self.matrix[list(test_indices)], axis=0)
        target_reqs = np.any(self.matrix, axis=0)
        return np.all(combined_coverage[target_reqs])

# --- Ejemplo de cálculo de métricas obligatorias ---
def calculate_metrics(original_size, selected_size, matrix, selected_indices):
    # TSSR: Test Suite Size Reduction
    tssr = 1 - (selected_size / original_size)
    
    # FDCLOSS: Fault Detection Capability Loss
    # Se aproxima por la cobertura total de requisitos
    u_t = np.sum(np.any(matrix, axis=0)) # Requisitos cubiertos por T
    u_s = np.sum(np.any(matrix[selected_indices], axis=0)) # Requisitos cubiertos por S
    fdcloss = 1 - (u_s / u_t) if u_t > 0 else 0
    
    return tssr, fdcloss