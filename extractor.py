import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        found_urls = set()
        
        # Interceptor de red por si el reproductor los carga mediante peticiones
        def handle_request(request):
            if ".m3u8" in request.url:
                found_urls.add(request.url)

        page.on("request", handle_request)
        
        try:
            # 1. Entrar a la página principal
            print("Entrando a universoreality.com...")
            await page.goto("https://universoreality.com/", timeout=60000)
            
            # 2. Hacer clic en el botón de cámaras usando su ID exacto (#btn-camaras)
            print("Haciendo clic en el botón de cámaras...")
            await page.click("#btn-camaras", timeout=10000)
            
            # 3. Esperar a que cargue la nueva página dinámicamente
            await page.wait_for_load_state("networkidle", timeout=15000)
            
            # 4. Extraer las URLs directamente de los atributos onclick de los botones (como en tu Imagen 1)
            buttons = await page.locator("button.camera-btn").all()
            for btn in buttons:
                onclick_attr = await btn.get_attribute("onclick")
                if onclick_attr:
                    # Extraer cualquier URL m3u8 dentro del atributo onclick
                    urls_in_onclick = re.findall(r"['\"](https?://[^'\"]+\.m3u8[^'\"]*)['\"]", onclick_attr)
                    for u in urls_in_onclick:
                        found_urls.add(u)
            
            # 5. Si por alguna razón no se capturaron estáticamente, hacemos clic en cada botón para forzar la red
            if not found_urls and buttons:
                print("Forzando clics en los botones de cámara...")
                for btn in buttons:
                    await btn.click()
                    await page.wait_for_timeout(2000)
                    
        except Exception as e:
            print("Error durante el proceso:", e)
            
        await browser.close()
        
        # Guardar todas las URLs encontradas en el archivo url.txt (separadas por saltos de línea)
        if found_urls:
            print(f"¡URLs encontradas con éxito!: {list(found_urls)}")
            with open("url.txt", "w") as f:
                for u in sorted(found_urls):
                    f.write(f"{u}\n")
        else:
            print("No se encontró ningún m3u8.")

asyncio.run(main())
