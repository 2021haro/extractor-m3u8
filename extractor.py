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
            # REEMPLAZA ESTA URL POR LA DE TU PÁGINA WEB OBJETIVO
            await page.goto("https://laurared.duckdns.org:40522/?_nocache=1790040160416", timeout=60000)
            await page.wait_for_timeout(10000)
        except Exception as e:
            print("Error cargando la página:", e)
            
        await browser.close()
        
        if m3u8_url:
            print(f"¡Encontrado!: {m3u8_url}")
            with open("url.txt", "w") as f:
                f.write(m3u8_url)
        else:
            print("No se encontró ningún m3u8.")

asyncio.run(main())
