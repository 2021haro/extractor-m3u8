import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        found_urls = set()
        
        def handle_request(request):
            if ".m3u8" in request.url:
                found_urls.add(request.url)

        page.on("request", handle_request)
        
        try:
            print("1. Entrando a universoreality.com...")
            await page.goto("https://universoreality.com/", timeout=60000)
            
            print("2. Esperando el botón de cámaras...")
            await page.wait_for_selector("#btn-camaras", timeout=20000)
            
            print("3. Haciendo clic en el botón de cámaras...")
            await page.click("#btn-camaras")
            
            # Esperar a que cargue la nueva página de DuckDNS
            await page.wait_for_timeout(6000)
            
            # Buscar botones de cámaras en la nueva página
            buttons = await page.locator("button.camera-btn").all()
            print(f"Botones de cámara encontrados: {len(buttons)}")
            
            for btn in buttons:
                onclick_attr = await btn.get_attribute("onclick")
                if onclick_attr:
                    urls = re.findall(r"['\"](https?://[^'\"]+\.m3u8[^'\"]*)['\"]", onclick_attr)
                    for u in urls:
                        found_urls.add(u)
                        
            # Si no se obtuvieron por el atributo, simulamos clics en los botones
            if not found_urls and buttons:
                print("Haciendo clic en las cámaras para forzar la captura...")
                for btn in buttons:
                    await btn.click()
                    await page.wait_for_timeout(3000)
                    
        except Exception as e:
            print(f"Aviso durante el proceso: {e}")
            
        await browser.close()
        
        # Escribir siempre el archivo url.txt para evitar errores de Git
        print("Guardando resultados en url.txt...")
        with open("url.txt", "w", encoding="utf-8") as f:
            if found_urls:
                print(f"¡URLs encontradas!: {list(found_urls)}")
                for u in sorted(found_urls):
                    f.write(f"{u}\n")
            else:
                f.write("No se encontraron enlaces m3u8 en esta ejecucion.\n")

asyncio.run(main())
