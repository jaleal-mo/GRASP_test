# Test Suite Minimization mediante el algoritmo GRASP


**Autores:**
- Duvan Dario Castro Bautista
- Iván Dario Cepeda Gomez
- José Antonio Leal Moreno

---

Esta sección describe el funcionamiento del algoritmo **GRASP (Greedy Randomized Adaptive Search Procedure)** aplicado al problema de **minimización de suites de prueba basada en cobertura de requisitos**.

El objetivo principal es reducir el número de tests manteniendo la cobertura total de requisitos, combinando estrategias *greedy*, aleatoriedad controlada y búsqueda local.

---

# Descripción del Problema y Requisitos

## Objetivo general

El objetivo de este trabajo es implementar un algoritmo basado en **GRASP (Greedy Randomized Adaptive Search Procedure)** para el problema de **reducción de test suites**, utilizando **cobertura de requisitos** como criterio principal de evaluación.

El algoritmo debe equilibrar dos objetivos contrapuestos:
- Reducir el tamaño de la suite de tests.
- Mantener la mayor capacidad de detección de fallos posible, aproximada mediante cobertura.

---

## Visión general del proceso

El algoritmo GRASP se compone de tres fases principales:

1. **Fase constructiva**: genera una solución inicial factible.
2. **Búsqueda local**: mejora la solución eliminando tests redundantes.
3. **Evaluación**: calcula métricas de calidad y rendimiento.

El proceso se repite varias veces usando diferentes semillas aleatorias para obtener soluciones más robustas.

---

## Diagrama de flujo del algoritmo GRASP

```
Inicio
│
▼
Leer matriz de cobertura Test–Requisito
│
▼
Identificar requisitos cubribles
│
▼
Para cada semilla (iteración GRASP):
│
├─► Fase Constructiva
│ │
│ ├─ Inicializar solución vacía
│ ├─ Mientras existan requisitos sin cubrir:
│ │ ├─ Calcular ganancia de cada test
│ │ ├─ Construir Lista Restringida de Candidatos (RCL)
│ │ ├─ Seleccionar un test aleatorio de la RCL
│ │ └─ Actualizar cobertura
│ │
│ └─ Solución inicial factible
│
├─► Búsqueda Local
│ │
│ ├─ Ordenar tests por menor cobertura
│ ├─ Intentar eliminar tests redundantes
│ └─ Mantener cobertura completa
│
├─► Evaluación de la solución
│ │
│ ├─ Calcular TSSR
│ ├─ Calcular FDCLOSS
│ └─ Medir tiempo de ejecución
│
▼
Seleccionar la mejor solución global
│
▼
Reportar resultados y estadísticas
│
▼
Fin
```
---

## Descripción de las fases del algoritmo

### Entrada del algoritmo

El algoritmo recibe como entrada una **matriz binaria de cobertura test–requisito**, donde:

- Las filas representan los tests.
- Las columnas representan los requisitos.
- Un valor `1` indica que el test cubre el requisito correspondiente.

---

### Identificación de requisitos cubribles

Antes de iniciar el proceso, se identifican los requisitos que pueden ser cubiertos por al menos un test.

Esto evita intentar cubrir requisitos imposibles, como:
- Errores en los datos.
- Requisitos obsoletos.
- Tests incompletos.
- Columnas totalmente en cero.

---

### Fase constructiva

La fase constructiva genera una solución inicial válida utilizando una estrategia *greedy aleatorizada*.

#### Funcionamiento general

1. Se inicia con una solución vacía.
2. Mientras existan requisitos cubribles sin cubrir:
   - Se calcula la **ganancia** de cada test.
   - Se construye la **Lista Restringida de Candidatos (RCL)**.
   - Se selecciona aleatoriamente un test dentro de la RCL.
   - Se actualiza la cobertura acumulada.

---

## ⚙️ Parámetros del algoritmo

En el algoritmo GRASP, cada test puede ser seleccionado **como máximo una vez**
durante la construcción de una solución.

El comportamiento del algoritmo durante la fase constructiva está controlado por
el parámetro \( \alpha \), el cual regula el equilibrio entre selección greedy y
aleatoriedad.

---

### Parámetro α (alpha)

El parámetro \( \alpha \) se estableció en **0.15** con el objetivo de favorecer la
**intensificación** durante la fase constructiva del algoritmo GRASP, priorizando
la selección de tests con alta ganancia de cobertura.

Este valor introduce un grado **controlado de aleatoriedad** mediante la
construcción de la **Lista Restringida de Candidatos (RCL)**, permitiendo explorar
distintas soluciones iniciales sin comprometer la calidad de la cobertura ni
incrementar innecesariamente el tamaño de la suite resultante.

En particular:
- \( \alpha \to 0 \) produce un comportamiento puramente greedy.
- \( \alpha \to 1 \) incrementa la aleatoriedad en la selección.
- \( \alpha = 0.15 \) ofrece un equilibrio adecuado entre calidad de solución y
  diversidad.

---

## Ganancia de un test en el algoritmo GRASP

### Definición breve

La **ganancia de un test** se define como el número de requisitos **aún no
cubiertos** que dicho test cubriría si se selecciona en la iteración actual.

En cada iteración, la ganancia se calcula considerando únicamente los requisitos
pendientes de cubrir, lo que permite priorizar los tests más útiles en ese
momento.

---

### ¿Qué significa la ganancia en GRASP?

En el algoritmo **GRASP (Greedy Randomized Adaptive Search Procedure)**, la
ganancia es una medida *greedy* utilizada durante la **fase constructiva
aleatorizada** para guiar la selección de tests.

Esta métrica permite:
- Favorecer tests con alta contribución de cobertura.
- Adaptar la selección conforme aumenta la cobertura acumulada.
- Mantener un equilibrio entre **intensificación** y **diversificación**.

---

### Definición formal

Sea:
- \( T \): conjunto total de tests.
- \( R \): conjunto de requisitos.
- \( S \subseteq T \): solución parcial construida hasta el momento.
- \( U(S) \subseteq R \): conjunto de requisitos ya cubiertos por la solución parcial.
- \( U(t) \subseteq R \): conjunto de requisitos cubiertos por un test \( t \).

La **ganancia** de un test \( t \in T \setminus S \) se define como:

\[
\text{ganancia}(t) = | U(t) \setminus U(S) |
\]

Es decir, el número de requisitos que el test \( t \) cubriría **por primera vez**
si se selecciona en la iteración actual.

---

### Intuición de la ganancia

- Un test con **ganancia alta** cubre muchos requisitos que aún no han sido
  cubiertos.
- Un test con **ganancia baja o cero** aporta poca o ninguna información nueva y
  suele ser menos prioritario.
- La ganancia es **adaptativa**: cambia en cada iteración a medida que aumenta la
  cobertura acumulada.

---

### ¿Cómo se calcula en el código?

En la implementación, la ganancia se calcula en dos pasos:

```python
# Índices de los requisitos aún no cubiertos y que son cubribles
uncovered_idx = np.where(~covered_reqs & target_reqs)[0]
```

## Ganancia marginal de cada test:
 número de requisitos no cubiertos que cubriría cada test
gains = np.sum(self.matrix[:, uncovered_idx], axis=1)

---

### Lista Restringida de Candidatos (RCL)

La RCL contiene los tests cuya ganancia es cercana a la mejor ganancia disponible.

El parámetro `α` controla el equilibrio entre:

- `α → 0`: comportamiento greedy puro.
- `α → 1`: selección casi aleatoria.

Este mecanismo permite explorar soluciones alternativas sin perder calidad.

---

### Búsqueda local

Una vez obtenida la solución inicial, se aplica una fase de **búsqueda local** para reducir aún más el tamaño de la suite.

#### Proceso

1. Los tests seleccionados se ordenan por menor cobertura.
2. Para cada test:
   - Se intenta eliminarlo temporalmente.
   - Si la cobertura total se mantiene, el test se descarta.
   - Si la cobertura se pierde, el test se conserva.

Esta fase elimina tests redundantes manteniendo la cobertura completa.

---

## Evaluación de la solución

La calidad de cada solución generada por el algoritmo GRASP se evalúa mediante
métricas cuantitativas basadas en **cobertura de requisitos**, **reducción del
tamaño de la suite de pruebas** y **eficiencia computacional**.

Dado que no se dispone de fallos reales, la capacidad de detección de errores se
aproxima utilizando la cobertura total de requisitos alcanzada por la suite
reducida.

### 1. Test Suite Size Reduction (TSSR)

Esta métrica mide el **grado de reducción** alcanzado respecto a la suite de
pruebas original.

Sea:
- \( |T| \): número de tests en la suite original.
- \( |S| \): número de tests seleccionados en la suite reducida.

La métrica se define como:

\[
TSSR = 1 - \frac{|S|}{|T|}
\]

**Interpretación**:
- Un valor cercano a **1** indica una reducción significativa del número de tests.
- Un valor de **0** indica que no se ha producido ninguna reducción.
- Valores negativos no son posibles.

Esta métrica permite evaluar directamente la **eficiencia estructural** de la
solución obtenida.

---

### 2. Fault Detection Capability Loss (FDCLOSS) basada en cobertura

Dado que no se dispone de información sobre fallos reales, la capacidad de
detección de fallos se aproxima mediante la **cobertura total de requisitos**.

Sea:
- \( Cov(t) \): conjunto de requisitos cubiertos por un test \( t \).
- \( U(S) = \bigcup_{t \in S} Cov(t) \): conjunto de requisitos cubiertos por la suite reducida.
- \( U(T) = \bigcup_{t \in T} Cov(t) \): conjunto de requisitos cubiertos por la suite original.

La métrica se define como:

\[
FDCLOSS = 1 - \frac{|U(S)|}{|U(T)|}
\]

**Interpretación**:
- Un valor de **0** indica que la suite reducida mantiene la cobertura total de
  requisitos.
- Valores mayores indican pérdida de cobertura y, por tanto, una disminución
  aproximada de la capacidad de detección de fallos.

El objetivo del algoritmo es **minimizar esta métrica**, idealmente manteniéndola
en cero.

### 3. Tiempo de ejecución

Además de las métricas basadas en cobertura, se mide el **tiempo de ejecución**
del algoritmo para cada ejecución.

Esta métrica permite evaluar la **eficiencia computacional** del enfoque propuesto
y analizar su viabilidad para suites de pruebas de gran tamaño.

---

## Repetición con múltiples semillas

El algoritmo GRASP se ejecuta múltiples veces usando diferentes semillas aleatorias con el fin de:

- Explorar diferentes soluciones.
- Reducir el impacto de la aleatoriedad.
- Obtener resultados estadísticamente representativos.

Finalmente, se reportan estadísticas agregadas como media, mínimo, máximo y desviación estándar.

---

## Observación final

La combinación de construcción greedy aleatorizada, búsqueda local y evaluación basada en cobertura permite a GRASP obtener soluciones eficientes y robustas para la minimización de suites de prueba, manteniendo la cobertura completa de requisitos con un menor número de tests.

---

## Requisitos
- **Lenguaje: ** Python 3.12
- **Dependencias: ** 
    - numpy

## Instalación de dependencias

Se recomienda utilizar un entorno virtual.

```
    pip install numpy
```

## Compilación

Este proyecto no requiere compilación previa, ya que está desarrollado en Python.

## Ejecución
```
    python main.py
```

## Entorno virtual
```
    python -m venv .venv
    .venv\Scripts\activate
```