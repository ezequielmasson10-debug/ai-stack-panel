# White House AI Stack — Panel de Análisis Cuantitativo

Panel web interactivo para el análisis de las 25 empresas del "White House AI Stack", organizadas en 5 sectores: Energía (VST, CEG, OKLO, EOSE, GEV), Chips & Computing (NVDA, AMD, TSM, MU, ARM), Cloud/Data Centers (NBIS, IREN, CRWV, APLD, CIFR), Modelos de IA (MSFT, GOOGL, META, AMZN, ORCL) y Aplicaciones (PLTR, TSLA, NOW, SNOW, CRM).

Cinco solapas: **Análisis Fundamental**, **Análisis Técnico**, **Optimización de Cartera**, **VaR & Performance** y **Backtesting & Machine Learning**. Las metodologías y parámetros replican fielmente los scripts Python del curso (RSI(14) con suavizado de Wilder, MACD(12,26,9), Bollinger SMA(20)±2σ, Keltner fórmula original 1960, Hurst rolling(100), frontera eficiente Monte Carlo con 10.000 carteras, VaR paramétrico/histórico/Monte Carlo con Cholesky, atribución Brinson-Hood-Beebower y Brinson-Fachler, backtests con costos de 15 bps y ejecución shift(1) anti look-ahead, walk-forward ML con árboles CART de profundidad 5).

## Archivos del repositorio

| Archivo | Función |
|---|---|
| `index.html` | El panel completo (autocontenido, se abre en cualquier navegador) |
| `actualizar_datos.py` | Script que descarga precios y fundamentales de Yahoo Finance y genera `datos_reales.json` |
| `datos_reales.json` | Datos de mercado del último cierre (lo genera y actualiza el workflow) |
| `.github/workflows/actualizar_datos.yml` | Automatización: corre el script de lunes a viernes a las 19:30 (hora Argentina) |
| `requirements.txt` | Dependencias de Python para el workflow |

## Cómo publicar el panel (una sola vez)

1. Crear un repositorio nuevo en GitHub (por ejemplo `ai-stack-panel`), público.
2. Subir todos los archivos de este kit **más** `index.html` y `actualizar_datos.py`. Se puede hacer desde la web con "Add file → Upload files" arrastrando los archivos y la carpeta `.github` completa.
3. Ir a **Settings → Pages → Source: Deploy from a branch → Branch: `main` / (root) → Save**.
4. En un minuto el panel queda publicado en `https://TU-USUARIO.github.io/ai-stack-panel/`.

## Actualización diaria automática

El workflow de GitHub Actions ejecuta `actualizar_datos.py` en los servidores de GitHub (gratis para repos públicos) de lunes a viernes a las 22:30 UTC (19:30 en Argentina), después del cierre de Wall Street, y commitea el `datos_reales.json` resultante. No hace falta tener ninguna computadora encendida.

Para probarlo sin esperar al horario: pestaña **Actions → Actualizar datos de mercado → Run workflow**.

Para cambiar el horario, editar la línea `cron:` del workflow (el formato es `minuto hora día-mes mes día-semana`, siempre en UTC; Argentina es UTC−3).

## Uso local (sin GitHub)

También se puede abrir `index.html` directamente en el navegador: funciona de inmediato con datos simulados. Para datos reales, correr `python actualizar_datos.py` y cargar el `datos_reales.json` generado con el botón "Cargar datos reales" del panel.

## Nota sobre los datos

La página indica en todo momento si está mostrando datos **simulados** (generados con estructura estadística realista) o **reales** (del último cierre descargado). Los datos de Yahoo Finance pueden tener demoras o huecos; el script incluye reintentos y tolerancia a fallos por ticker.
