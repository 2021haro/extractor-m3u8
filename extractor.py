import asyncio
import re
from playwright.async_api import async_playwright

async def main():
    # 1. Crear el archivo url.txt de inmediato para blindar Git ante cualquier fallo
    with open("url.txt", "w", encoding="utf-8") as f:
        f.write("Iniciando extraccion con navegador...\n")

    found_urls = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Interceptar peticiones de red por si el reproductor carga el m3u8 dinámicamente
        def handle_request(request):
            if ".m3u8" in request.url:
                found_urls.add(request.url)

        page.on("request", handle_request)

        try:
            print("1. Entrando a universoreality.com...")
            await page.goto("https://universoreality.com/", timeout=60000)

            print("2. Esperando el botón de cámaras (#btn-camaras)...")
            await page.wait_for_selector("#btn-camaras", timeout=20000)

            print("3. Haciendo clic en el botón de cámaras...")
            # Usamos expect_navigation para esperar que abra la nueva página de DuckDNS
            async with page.expect_navigation(timeout=30000):
                await page.click("#btn-camaras")

            print("4. Esperando a que carguen los botones de cámara...")
            await page.wait_for_selector("button.camera-btn", timeout=20000)
            await page.wait_for_timeout(3000)

            # Extraer las URLs directamente de los atributos onclick de los botones
            buttons = await page.locator("button.camera-btn").all()
            print(f"Botones de cámara detectados: {len(buttons)}")

            for btn in buttons:
                onclick_attr = await btn.get_attribute("onclick")
                if onclick_attr:
                    urls = re.findall(r"['\"](https?://[^'\"]+\.m3u8[^'\"]*)['\"]", onclick_attr)
                    for u in urls:
                        found_urls.add(u)

            # Si por alguna razón el atributo no bastó, hacemos clic en cada cámara para forzar el tráfico
            if not found_urls and buttons:
                print("Forzando clics en las cámaras...")
                for btn in buttons:
                    await btn.click()
                    await page.wait_for_timeout(2000)

        except Exception as e:
            print(f"⚠️ Aviso durante la ejecución del navegador: {e}")

        await browser.close()

    # 2. Guardar los resultados definitivos en url.txt
    with open("url.txt", "w", encoding="utf-8") as f:
        if found_urls:
            print(f"✅ ¡URLs encontradas con éxito!: {list(found_urls)}")
            for u in sorted(found_urls):
                f.write(f"{u}\n")
        else:
            print("⚠️ No se capturó ningún m3u8 en esta ejecución.")
            f.write("No se encontro ningun m3u8 en esta ejecucion.\n")

asyncio.run(main())
