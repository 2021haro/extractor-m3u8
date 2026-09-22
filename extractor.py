import re
import requests

def main():
    print("🚀 Iniciando script de extracción...")
    
    # Crear el archivo url.txt de inmediato para evitar errores de Git
    with open("url.txt", "w", encoding="utf-8") as f:
        f.write("Iniciando busqueda...\n")

    found_urls = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
    }

    try:
        print("1. Consultando universoreality.com...")
        response = requests.get("https://universoreality.com/", headers=headers, timeout=30)
        print(f"📡 Código HTTP principal: {response.status_code}")

        if response.status_code != 200:
            print(f"⚠️ La página principal respondió con estado: {response.status_code}")
            return

        html_main = response.text

        # Buscar el enlace (href) del botón #btn-camaras
        match_href = re.search(r'id=["\']btn-camaras["\'][^>]*href=["\']([^"\']+)["\']', html_main)
        if not match_href:
            match_href = re.search(r'href=["\']([^"\']+)["\'][^>]*id=["\']btn-camaras["\']', html_main)

        if match_href:
            camaras_url = match_href.group(1)
            print(f"2. 🔗 Enlace de cámaras encontrado: {camaras_url}")

            # Consultar la página de las cámaras (DuckDNS)
            print("3. Consultando la página dinámica de cámaras...")
            resp_cam = requests.get(camaras_url, headers=headers, timeout=30)
            print(f"📡 Código HTTP cámaras: {resp_cam.status_code}")

            html_cam = resp_cam.text

            # Buscar todas las URLs .m3u8 en el código fuente de las cámaras
            m3u8_matches = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html_cam)
            print(f"🔍 Coincidencias m3u8 detectadas: {len(m3u8_matches)}")

            for u in m3u8_matches:
                clean_url = re.sub(r'[\'").]+$', '', u)
                found_urls.add(clean_url)
        else:
            print("⚠️ No se encontró el botón #btn-camaras. Buscando m3u8 directamente en la principal...")
            m3u8_matches = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html_main)
            for u in m3u8_matches:
                found_urls.add(re.sub(r'[\'").]+$', '', u))

    except Exception as e:
        print(f"❌ Ocurrió un error durante la petición: {e}")

    # Escribir los resultados finales en url.txt
    with open("url.txt", "w", encoding="utf-8") as f:
        if found_urls:
            print(f"✅ ¡URLs encontradas y guardadas!: {list(found_urls)}")
            for u in sorted(found_urls):
                f.write(f"{u}\n")
        else:
            print("⚠️ No se encontraron enlaces m3u8 en esta ejecución.")
            f.write("No se encontraron enlaces m3u8 en esta ejecución.\n")

if __name__ == "__main__":
    main()
