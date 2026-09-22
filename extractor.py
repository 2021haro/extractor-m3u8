import re
import requests

def main():
    # 1. Crear el archivo url.txt de inmediato por seguridad
    with open("url.txt", "w", encoding="utf-8") as f:
        f.write("Iniciando busqueda de enlaces m3u8...\n")

    found_urls = set()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    try:
        print("1. Consultando universoreality.com...")
        response = requests.get("https://universoreality.com/", headers=headers, timeout=30)
        response.raise_for_status()
        html_main = response.text

        # Buscar el enlace (href) del botón #btn-camaras
        match_href = re.search(r'id=["\']btn-camaras["\'][^>]*href=["\']([^"\']+)["\']', html_main)
        if not match_href:
            match_href = re.search(r'href=["\']([^"\']+)["\'][^>]*id=["\']btn-camaras["\']', html_main)

        if match_href:
            camaras_url = match_href.group(1)
            print(f"2. Enlace de cámaras encontrado: {camaras_url}")

            # Consultar la página de las cámaras en DuckDNS
            print("3. Extrayendo los m3u8 de la página de cámaras...")
            resp_cam = requests.get(camaras_url, headers=headers, timeout=30)
            resp_cam.raise_for_status()
            html_cam = resp_cam.text

            # Buscar todas las URLs .m3u8 en el código fuente
            m3u8_matches = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html_cam)
            for u in m3u8_matches:
                clean_url = re.sub(r'[\'").]+$', '', u)
                found_urls.add(clean_url)
        else:
            print("⚠️ No se encontró el botón #btn-camaras, buscando en la principal...")
            m3u8_matches = re.findall(r'https?://[^\s\'"]+\.m3u8[^\s\'"]*', html_main)
            for u in m3u8_matches:
                found_urls.add(re.sub(r'[\'").]+$', '', u))

    except Exception as e:
        print(f"❌ Error en la petición: {e}")

    # Guardar resultados limpios en url.txt
    if found_urls:
        print(f"¡URLs encontradas con éxito!: {list(found_urls)}")
        with open("url.txt", "w", encoding="utf-8") as f:
            for u in sorted(found_urls):
                f.write(f"{u}\n")
    else:
        print("⚠️ No se encontró ningún m3u8.")
        with open("url.txt", "w", encoding="utf-8") as f:
            f.write("No se encontraron enlaces m3u8 en esta ejecución.\n")

if __name__ == "__main__":
    main()
