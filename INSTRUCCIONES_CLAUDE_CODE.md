# Instrucciones para pasarle a Claude Code

Este ZIP ya contiene TODOS los archivos listos, en su ubicación final. No hay que armar nada más —
solo hay que publicarlo en GitHub. Pegale esto a Claude Code, parado dentro de esta carpeta descomprimida:

---

> Tenés en esta carpeta un panel de análisis financiero completo (`index.html`, `actualizar_datos.py`,
> `.github/workflows/actualizar_datos.yml`, `README.md`, `requirements.txt`, `.gitignore`). Quiero que:
>
> 1. Verifiques que tengo `gh` (GitHub CLI) autenticado con `gh auth status`; si no, guiame para autenticar.
> 2. Crees un repositorio público nuevo en mi cuenta de GitHub llamado `ai-stack-panel` con
>    `gh repo create ai-stack-panel --public --source=. --remote=origin`.
> 3. Hagas `git add`, `git commit` y `git push` de todos los archivos de esta carpeta, incluyendo la
>    carpeta `.github/` completa (verificá que no quede excluida por el `.gitignore`).
> 4. Actives GitHub Pages desde la rama `main` y carpeta raíz, usando
>    `gh api -X POST repos/{owner}/{repo}/pages -f "source[branch]=main" -f "source[path]=/"`
>    (o el equivalente si esa API cambió).
> 5. Me confirmes la URL final donde queda publicado (formato
>    `https://TU-USUARIO.github.io/ai-stack-panel/`) y verifiques con `gh api` que el workflow
>    `.github/workflows/actualizar_datos.yml` quedó registrado en Actions.

---

## Qué hace cada pieza una vez publicado

- **`index.html`**: el panel completo. Arranca con datos simulados (banner ámbar). Funciona standalone,
  no necesita servidor ni backend.
- **`actualizar_datos.py`**: descarga datos de Yahoo Finance y genera `datos_reales.json`.
- **`.github/workflows/actualizar_datos.yml`**: hace correr ese script automáticamente de lunes a viernes
  a las 19:30 (hora Argentina) en los servidores de GitHub, y commitea el JSON actualizado. **No requiere
  que ninguna computadora esté prendida.**
- Cuando el JSON se actualiza en el repo, para que el panel lo muestre automáticamente hay que abrirlo
  y usar el botón "Cargar datos reales (JSON)" apuntando al `datos_reales.json` del repo (se puede
  descargar con un click desde GitHub, o accediendo a la URL raw). Si en el futuro querés que la carga
  sea 100% automática al abrir la página (sin tocar el botón), pedímelo y agrego un `fetch()` al
  `datos_reales.json` del propio repo al cargar `index.html`.

## Verificación ya hecha

Antes de entregar este kit, el `index.html` fue ejecutado en un DOM simulado (Node + jsdom) navegando
las 5 solapas con distintas combinaciones de tickers (incluyendo las 25 empresas a la vez) sin errores
de JavaScript, y el `actualizar_datos.py` fue validado con `py_compile`. Aun así, recomendamos abrir el
panel una vez en el navegador después de publicado para confirmar visualmente los gráficos (Plotly.js
se carga desde un CDN externo, que no estaba disponible en el entorno de prueba).
