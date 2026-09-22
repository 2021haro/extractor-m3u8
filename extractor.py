import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        m3u8_url = None
        
        def handle_request(request):
            nonlocal m3u8_url
            if ".m3u8" in request.url:
                m3u8_url = request.url

        page.on("request", handle_request)
        
        try:
            # 1. Entra a la página web
            await page.goto("https://laurared.duckdns.org:40522/?_nocache=1790040160416", timeout=60000)
            
            # 2. ESPERAR Y HACER CLIC EN EL BOTÓN DE REPRODUCIR
            # (Elige una de las dos opciones de abajo según te convenga)
            
            # Opción A: Si el botón tiene un texto visible como "Play", "Reproducir", "Ver", etc.
            await page.get_by_text("CAM 1", exact=False).click(timeout=10000)
            
            # Opción B (Comenta la A y descomenta esta si prefieres usar un selector CSS o ID):
            # await page.click("#btn-play", timeout=10000)
            
            # 3. Esperar unos segundos después del clic para que capture el m3u8
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print("Error durante la ejecución:", e)
            
        await browser.close()
        
        if m3u8_url:
            print(f"¡Encontrado!: {m3u8_url}")
            with open("url.txt", "w") as f:
                f.write(m3u8_url)
        else:
            print("No se encontró ningún m3u8.")

asyncio.run(main())
