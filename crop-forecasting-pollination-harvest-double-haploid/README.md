# 🌾 Pipeline de Machine Learning: Pronóstico Operativo de Polinización, Cosecha y Doble Haploide

Este módulo contiene pipelines de Machine Learning y scripts en Python (`.py`) para la extracción, procesamiento y modelado predictivo de procesos agrícolas y mejoramiento genético vegetal (Programa Double Haploid, Arica - Chile).

---

## 🎯 Objetivo de Negocio e Impacto Operativo
El propósito principal de este sistema analítico es **pronosticar con al menos 2 semanas de anticipación** las fechas exactas de polinización y cosecha para:
* **Estimación de Carga Operativa:** Proyectar el volumen de material biológico que ingresará al laboratorio de Doble Haploide (DH).
* **Planificación de Recursos Humanos:** Proveer a la gerencia de laboratorio métricas anticipadas para la contratación, programación y dimensionamiento del personal operativo sin incurrir en cuellos de botella ni sobrecostos.

---

## ⚙️ Arquitectura del Pipeline

1. **Ingestión de Datos:** Extracción y procesamiento automatizado desde la base de datos relacional de producción (`QUEUE`).
2. **Transformación & Feature Engineering:** Limpieza de datos agronómicos, tratamiento de series temporales y construcción de variables predictivas.
3. **Modelado con Machine Learning:** Entrenamiento de algoritmos ML supervisados para la generación automática de pronósticos de fechas y carga de trabajo.

---

## 🔬 Módulos y Modelos ML Implementados

* 🐝 **Pronóstico de Polinización (*Pollination Forecasting*):**
  * Sincronización de floración y predicción de ventanas óptimas para cruces.
* 🚜 **Proyección de Cosecha & Carga de Laboratorio (*Harvest & Yield Prediction*):**
  * Modelos predictivos para calcular fechas estimadas de cosecha, volumen de muestras e ingreso de material al laboratorio.
* 🧫 **Eficiencia en Doble Haploide (*Double Haploid - DH / Haploídia*):**
  * Algoritmos de seguimiento para analizar la tasa de éxito en la inducción de haploídia, rescate de embriones y fijación de líneas puras.

---

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3 (`.py` scripts modularizados).
* **Machine Learning & Ciencia de Datos:** Scikit-learn, Pandas, NumPy, Statsmodels.
* **Bases de Datos:** SQL / Extracción y estructuración desde base de datos relacional `QUEUE`.

---

> **Nota de Confidencialidad:** Los scripts presentados ejecutan la arquitectura de pipelines y algoritmos de ML sobre estructuras de datos anonimizadas/simuladas para resguardar la confidencialidad de la base de datos corporativa.
