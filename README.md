# Test Suite Minimization - Algoritmo GRASP

**Grupo:**
- Duvan 
- Iván Cepeda
- José Antonio Leal Moreno


# Descripción del Problema y Requisitos

## Objetivo general

El objetivo de este trabajo es implementar un algoritmo basado en **GRASP (Greedy Randomized Adaptive Search Procedure)** para el problema de **reducción de test suites**, utilizando **cobertura de requisitos** como criterio principal de evaluación.

El algoritmo debe equilibrar dos objetivos contrapuestos:
- Reducir el tamaño de la suite de tests.
- Mantener la mayor capacidad de detección de fallos posible, aproximada mediante cobertura.

---

## Algoritmo requerido: GRASP

La solución debe implementar un algoritmo GRASP que combine explícitamente las siguientes fases:

### 1. Fase constructiva greedy aleatorizada
- La construcción de la solución debe basarse en un criterio **greedy**, utilizando la cobertura de requisitos.
- Se debe introducir **aleatoriedad** mediante una **Restricted Candidate List (RCL)**, de la cual se seleccionan candidatos de forma aleatoria.
- Esta fase genera una solución inicial factible.

### 2. Fase de mejora local
- A partir de la solución construida, se debe aplicar una **búsqueda local** para mejorarla.
- La mejora local busca optimizar la solución sin aumentar significativamente el coste computacional.
- Esta fase permite refinar la solución obtenida en la construcción.

### 3. Iteraciones
- El proceso completo (construcción + mejora local) debe repetirse varias veces.
- El algoritmo debe conservar la **mejor solución global** encontrada a lo largo de las iteraciones.

---

## Contexto del problema

- Se parte de una **suite de tests original** \( T \).
- Cada test cubre un conjunto de **requisitos**.
- La solución del algoritmo es una **suite reducida** \( S \subseteq T \).
- No se dispone de fallos reales, por lo que la capacidad de detección de fallos se aproxima mediante **cobertura de requisitos**.

---

## Métricas obligatorias

El trabajo debe reportar, como mínimo, las siguientes métricas, calculadas en base a cobertura:

### 1. Test Suite Size Reduction (TSSR)

Sea:
- \( |T| \): número de tests en la suite original.
- \( |S| \): número de tests seleccionados en la suite reducida.

La métrica se define como:

\[
TSSR = 1 - \frac{|S|}{|T|}
\]

**Interpretación**:
- Valores altos indican una mayor reducción de la suite.
- Un valor de 0 indica que no hubo reducción.

---

### 2. Fault Detection Capability Loss (FDCLOSS) basada en cobertura

Dado que no se dispone de fallos reales, la capacidad de detección de fallos se aproxima mediante la cobertura total de requisitos.

Sea:
- \( Cov(t) \): conjunto de requisitos cubiertos por un test \( t \).
- \( U(S) = \bigcup_{t \in S} Cov(t) \): conjunto de requisitos cubiertos por la suite reducida.
- \( U(T) = \bigcup_{t \in T} Cov(t) \): conjunto de requisitos cubiertos por la suite original.

La métrica se define como:

\[
FDCLOSS = 1 - \frac{|U(S)|}{|U(T)|}
\]

**Interpretación**:
- Un valor de 0 indica que no se ha perdido cobertura.
- Valores altos indican una mayor pérdida de capacidad de detección.

---

## Resultados esperados

Para cada instancia del problema, se espera reportar:
- El tamaño de la suite original \( |T| \).
- El tamaño de la suite reducida \( |S| \).
- El valor de **TSSR**.
- El valor de **FDCLOSS**.

Estas métricas permiten analizar el compromiso entre reducción de la suite y pérdida de cobertura.

## Parametros

En Grasp cada test solo puede seleccionarse una vez.

### Alpha

El parámetro α se estableció en 0.15 con el objetivo de favorecer la intensificación durante la fase constructiva del algoritmo GRASP, privilegiando la selección de tests con alta ganancia de cobertura. Este valor introduce un grado controlado de aleatoriedad mediante la Lista Restringida de Candidatos (RCL), permitiendo explorar distintas soluciones iniciales sin comprometer la calidad de la cobertura ni aumentar innecesariamente el tamaño de la suite resultante.


## Requisitos
- **Lenguaje: ** Python 3.12
- **Dependencias: ** 
    - numpy

## Instalación
``bash
        pip install numpy

## Ejecución
``bash
    python main.py


## Entorno virtual
``bash
    python -m venv .venv
    .venv\Scripts\activate