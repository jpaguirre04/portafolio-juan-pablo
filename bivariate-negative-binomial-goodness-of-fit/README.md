# 📊 Test de Ajuste y Robustez Estadística: Distribución Binomial Negativa Bivariada

Este módulo contiene algoritmos desarrollados en **R** para la construcción, evaluación de potencia y validación de pruebas de bondad de ajuste (*Goodness-of-Fit*) sobre modelos de **Binomial Negativa Bivariada**, aplicados a datos de conteo con dependencia y sobredispersión.

---

## 💡 Relevancia y Aplicación en Riesgo y Finanzas
En modelado de riesgos, seguros y finanzas cuantitativas, es vital analizar dos variables correlacionadas (ej. frecuencia de reclamos simultáneos o eventos de impago acoplados). Este proyecto evalúa la confiabilidad del test estadístico para garantizar que la distribución supuesta responda con precisión antes de ser usada en producción.

---

## 🔬 Módulos y Metodología en R

### 1. Calibración y Error Tipo I (Control de Falsos Positivos)
Evaluación empírica de la tasa de error Tipo I bajo tres métodos de estimación de parámetros:
* **Método de los Momentos (MOM)**
* **Máxima Verosimilitud (MLE)**
* **Método de Doble Cero (Zero-Proportion)**

### 2. Análisis de Potencia del Test (Power Analysis)
Estudio de simulación Monte Carlo para medir la capacidad del test de detectar desviaciones frente a diversas familias de **distribuciones bivariadas alternativas**:
* Bivariada de **Hermite**
* Bivariada **Gaussiana Inversa**
* Bivariada de **Serie Logarítmica**
* Bivariada **Binomial Negativa**
* Bivariada **Neyman Tipo A**
* Bivariada de **Poisson**

---

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** R (`.R` scripts modularizados).
* **Técnicas:** Simulación Monte Carlo, Estimación por Máxima Verosimilitud (MLE), Pruebas de Hipótesis y Ajuste de Distribuciones Multivariadas.
