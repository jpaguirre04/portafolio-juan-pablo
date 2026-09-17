# 📈 Macroeconomic Liquidity Quadrant (Hedgeye Framework) & Macro Forecasting

Este módulo contiene scripts en Python (`.py`) diseñados para la extracción automatizada de indicadores macroeconómicos desde la **FRED API** (Federal Reserve Bank of St. Louis) para la estimación de tendencias de Crecimiento (**GDP / PIB**) e Inflación (**CPI / IPC**) y la gestión de liquidez trimestral.

---

## 🎯 Objetivo Financiero & Modelo Analítico
* **Enfoque Cuadrante Macro (Hedgeye Style):** Mapeo trimestral de la economía en 4 cuadrantes (Quad 1 a Quad 4) analizando la aceleración o desaceleración combinada del Crecimiento y la Inflación.
* **Toma de Decisiones de Liquidez:** Proveer señales cuantitativas para anticipar regímenes macroeconómicos, ajustar la estructura de liquidez y gestionar exposición de riesgo en mesa de dinero.

---

## ⚙️ Arquitectura del Script

1. **Ingestión API (FRED):** Conexión y extracción de series temporales macroeconómicas públicas (GDP, CPI, tasas de interés, agregados monetarios).
2. **Procesamiento & Normalización:** Cálculo de tasas de variación interanual (YoY), aceleración/desaceleración y tasas de cambio trimestrales.
3. **Generación del Cuadrante & Visualización:** Clasificación automática del régimen macroeconómico actual y proyectado para soporte en la toma de decisiones.

---

## 🛠️ Tecnologías y Herramientas
* **Lenguaje:** Python 3 (`.py` scripts modularizados).
* **Integraciones:** FRED API (`pandas_datareader` / `fredapi`).
* **Análisis de Datos & Visualización:** Pandas, NumPy, Matplotlib / Seaborn.

---

> **Nota:** Los scripts utilizan únicamente series de tiempo públicas de la FRED API. Las estrategias específicas de posicionamiento privado han sido omitidas para resguardar la confidencialidad.
