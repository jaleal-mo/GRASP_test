# import numpy as np

# def apply_reductions(matrix, mode='C'):
#     """
#     Aplica reducciones y devuelve la matriz junto con el mapeo de tests originales.
#     """
#     m = matrix.copy()
#     # Mantenemos un rastro de qué fila de la matriz actual es qué test original
#     test_mapping = np.arange(matrix.shape[0])
    
#     # Regla A: Reducción de Casos de Prueba 
#     if mode in ['A', 'C']:
#         # 1. Eliminar tests vacíos
#         mask_not_empty = np.any(m == 1, axis=1)
#         m = m[mask_not_empty]
#         test_mapping = test_mapping[mask_not_empty]
        
#         # 2. Eliminar tests duplicados
#         _, unique_idx = np.unique(m, axis=0, return_index=True)
#         sorted_unique = np.sort(unique_idx)
#         m = m[sorted_unique]
#         test_mapping = test_mapping[sorted_unique]
        
#     # Regla B: Reducción de Requisitos (solo afecta a la matriz interna del solver) 
#     if mode in ['B', 'C']:
#         _, unique_reqs = np.unique(m, axis=1, return_index=True)
#         m = m[:, np.sort(unique_reqs)]
        
#     return m, test_mapping


import numpy as np

def apply_reductions(matrix, mode='C'):
    """
    Aplica reducciones según el modo:
    A: Solo reducción de tests (filas).
    B: Solo reducción de requisitos (columnas).
    C: Ambas (Tests y Requisitos).
    """
    # Realiza una copia de la matriz inicial para evitar trabajar sobre ella.
    m = matrix.copy()
    # Mapeo inicial: mapping[i] = i
    test_mapping = np.arange(matrix.shape[0])
    
    # --- REDUCCIÓN DE TESTS (Modo A o C) ---
    if mode in ['A', 'C']:
       
        # 1. Eliminar tests vacíos por fila (no cubren nada)
        # Preserva la relación con índices originales
        mask_not_empty = np.any(m == 1, axis=1)
        m = m[mask_not_empty]
        test_mapping = test_mapping[mask_not_empty]
        
        # 2. Eliminar tests duplicados (filas idénticas) -- axis = 0 => compara filas
        # Devuelve el primer indice de cada fila única
        # Usamos return_index para mantener el orden original
        _, unique_idx = np.unique(m, axis=0, return_index=True)
        unique_idx = np.sort(unique_idx)
        m = m[unique_idx]
        test_mapping = test_mapping[unique_idx]
        
    # --- REDUCCIÓN DE REQUISITOS (Modo B o C) ---
    if mode in ['B', 'C']:
        # Eliminar requisitos duplicados (columnas idénticas) -- axis = 1 => compara columnas
        # Reduce el número de columnas y no afecta al número de tests.
        _, unique_col_idx = np.unique(m, axis=1, return_index=True)
        m = m[:, np.sort(unique_col_idx)]
        
        # Opcional: Eliminar requisitos que nadie cubre (columnas de ceros)
        mask_req_cubrible = np.any(m == 1, axis=0)
        m = m[:, mask_req_cubrible]
        
    # Devuelve:
    # - m: matriz binaria reducida tras aplicar las reducciones seleccionadas.
    #      Las filas representan los tests activos y las columnas los requisitos relevantes.
    # - test_mapping: vector de índices que permite mapear cada fila de 'm'
    #      al índice correspondiente del test original en la matriz de entrada.
    return m, test_mapping