import numpy as np
import random
import time

class GRASPSolver:


    def __init__(self, matrix, seed):
        # Guarda la matrix 
        self.matrix = matrix  # Filas = Tests, Columnas = Requisitos
        # num_tests = filas (tests), num_reqs = columnas (requisitos)
        self.num_tests, self.num_reqs = matrix.shape
        # Guarda la semilla
        self.seed = seed
        # Inicializa la aleatoridad 
        # permite múltiples ejecuciones independientes para explorar el espacio de soluciones
        random.seed(seed)
        np.random.seed(seed)



    def solve(self, alpha=0.1):
        """
        Ejecuta una iteración completa del algoritmo GRASP.

        El método aplica secuencialmente una fase constructiva greedy aleatorizada y una
        fase de mejora mediante búsqueda local, con el objetivo de obtener un subconjunto
        de tests que cubra todos los requisitos con el menor tamaño posible. Además,
        se mide el tiempo total de ejecución del algoritmo.

        Parameters
        ----------
        alpha : float, optional
            Parámetro de aleatoriedad (0 ≤ α ≤ 1) que controla la construcción de la
            Lista Restringida de Candidatos (RCL) en la fase constructiva.
            Por defecto, α = 0.1.

        Returns
        -------
        tuple
            - solution : list
                Lista de índices de los tests seleccionados que conforman la solución final.
            - execution_time : float
                Tiempo total de ejecución del algoritmo GRASP en segundos.
        """
        
        # Tiempo inicial del algoritmo Grasp
        start_time = time.time()
        
        # 1. Fase Constructiva Aleatorizada 
        solution = self._constructive_phase(alpha)
        
        # 2. Fase de Mejora (Búsqueda Local) 
        solution = self._local_search(solution)
        
        execution_time = time.time() - start_time
        return solution, execution_time
    


    def _constructive_phase(self, alpha):
        """
        Fase constructiva greedy aleatorizada del algoritmo GRASP.

        Construye una solución inicial seleccionando iterativamente tests que maximizan
        la ganancia de cobertura sobre los requisitos aún no cubiertos. En cada iteración,
        se define una Lista Restringida de Candidatos (RCL) controlada por el parámetro α,
        desde la cual se selecciona aleatoriamente el siguiente test.

        La fase finaliza cuando todos los requisitos cubribles han sido cubiertos.

        Parameters
        ----------
        alpha : float
            Parámetro de aleatoriedad (0 ≤ α ≤ 1) que controla el equilibrio entre
            comportamiento greedy y diversificación durante la construcción de la solución.

        Returns
        -------
        list
            Lista de índices de los tests seleccionados que conforman la solución inicial.
        """

        # Conjunto para almacenar los tests seleccionados (evita duplicados)
        solution = set()

        # Vector booleano que indica qué requisitos ya han sido cubiertos
        covered_reqs = np.zeros(self.num_reqs, dtype=bool)

        # Identifica los requisitos que son realmente cubribles
        # (excluye columnas totalmente en cero o requisitos inválidos)
        target_reqs = np.any(self.matrix, axis=0) 
        
        # Mientras existan requisitos cubribles sin cubrir,
        # se siguen seleccionando tests
        while not np.all(covered_reqs[target_reqs]):
            
            # Índices de los requisitos aún no cubiertos
            uncovered_idx = np.where(~covered_reqs & target_reqs)[0]

            # Ganancia marginal de cada test:
            # número de nuevos requisitos que cubriría
            gains = np.sum(self.matrix[:, uncovered_idx], axis=1)
            
            # Mejor y peor test útil según ganancia
            max_g = np.max(gains)
            min_g = np.min(gains[gains > 0]) if np.any(gains > 0) else 0
            
            # Umbral minimo para construir la Lista Restringida de Candidatos (RCL)
            # alpha controla el balance entre:
            # - alpha → 0 : selección greedy pura
            # - alpha → 1 : selección más aleatoria
            threshold = max_g - alpha * (max_g - min_g)

            # RCL (Restricted Candidate List): 
            # tests cuya ganancia supera el umbral 
            rcl = np.where(gains >= threshold)[0]
            
            # Selección aleatoria de un test dentro de los mejores candidatos
            selected_test = random.choice(rcl)
            solution.add(selected_test)
            
             # Actualiza la cobertura acumulada de requisitos
            covered_reqs |= self.matrix[selected_test].astype(bool)
            
        return list(solution)

    def _local_search(self, solution):
        """
        Fase de mejora (búsqueda local) del algoritmo GRASP.

        A partir de una solución factible obtenida en la fase constructiva,
        este método intenta reducir el tamaño de la suite eliminando tests
        redundantes. Para cada test de la solución, se evalúa si puede ser
        removido sin perder la cobertura total de los requisitos.

        El procedimiento:
        1. Ordena los tests seleccionados priorizando aquellos con menor cobertura,
            ya que son más candidatos a ser redundantes.
        2. Intenta eliminar cada test de forma iterativa.
        3. Mantiene la eliminación solo si la solución resultante sigue cubriendo
            todos los requisitos cubribles.

        Parámetros:
        - solution (list[int]): índices de los tests seleccionados tras la fase
            constructiva.

        Retorna:
        - list[int]: solución mejorada con el menor número posible de tests,
            manteniendo la cobertura completa.
        """

        # Ordena los tests seleccionados de menor a mayor cobertura de requisitos.
        # Los tests que cubren menos requisitos son evaluados primero, ya que son
        # más propensos a ser redundantes y eliminables.
        improved_solution = sorted(solution, key=lambda x: np.sum(self.matrix[x]), reverse=False)

        # Conjunto mutable que representa la solución actual durante la búsqueda local
        final_s = set(improved_solution)
        
        # Recorre los tests ordenados por menor cobertura y evalúa si pueden eliminarse
        for test in improved_solution:
            # Crea una solución temporal sin el test actual
            temp_solution = final_s - {test}
            # Si al eliminar el test se mantiene la cobertura completa de requisitos,
            # el test se considera redundante y se elimina definitivamente
            if self._check_full_coverage(temp_solution):
                final_s = temp_solution
                
        return list(final_s)

    def _check_full_coverage(self, test_indices):
        """
        Verifica si un conjunto de tests mantiene la cobertura completa
        de todos los requisitos cubribles.

        El método combina la cobertura de los tests seleccionados y comprueba
        que todos los requisitos que pueden ser cubiertos en la matriz original
        siguen estando cubiertos tras eliminar uno o más tests.

        Parámetros:
        - test_indices (set[int] | list[int]): índices de los tests a evaluar.

        Retorna:
        - bool: True si el conjunto de tests cubre todos los requisitos cubribles,
            False en caso contrario o si el conjunto está vacío.
        """
        # Si no hay tests seleccionados, no puede existir cobertura completa
        if not test_indices: 
            return False
        
        # Combina la cobertura de todos los tests seleccionados.
        # El resultado indica qué requisitos están cubiertos por al menos un test.
        combined_coverage = np.any(self.matrix[list(test_indices)], axis=0)

        # Identifica los requisitos que son cubribles en la matriz original
        # (columnas que tienen al menos un 1)
        target_reqs = np.any(self.matrix, axis=0)

        # Verifica que todos los requisitos cubribles estén cubiertos
        # por la solución actual
        return np.all(combined_coverage[target_reqs])



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