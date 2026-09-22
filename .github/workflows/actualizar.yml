name: Auto Extractor m3u8

on:
  schedule:
    - cron: '0 */6 * * *'
  workflow_dispatch:

jobs:
  run-extractor:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - name: Checkout del repositorio
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Instalar dependencias y navegador
        run: |
          pip install playwright
          playwright install chromium
          playwright install-deps

      - name: Ejecutar script de extracción
        run: python extractor.py

      - name: Asegurar archivo url.txt
        run: touch url.txt

      - name: Guardar y actualizar en GitHub
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.io"
          git add url.txt
          git diff --quiet && git diff --staged --quiet || (git commit -m "Actualizar URL m3u8 automática" && git push)
