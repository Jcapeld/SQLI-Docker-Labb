# SQLi Lab (Docker + MySQL) — UNION / Blind Boolean / Blind Time / Error-based

⚠️ Este laboratorio es **intencionadamente vulnerable**. Úsalo SOLO en local y aislado.

## Requisitos
- Docker + Docker Compose

## Arranque
```bash
cd sqli-lab-docker
docker compose up --build
```

Abre:
- http://localhost:8080

## Reset rápido (borrar datos)
```bash
docker compose down -v
docker compose up --build
```

## Endpoints del lab
- UNION-based:      /products?category=Gifts
- Blind Boolean:    /  (usa cookie TrackingId)
- Blind Time:       /search?q=anything
- Error-based:      /account?id=1

## Flags
- Flag1 (UNION):    tabla users (admin) -> extraer `administrator`
- Flag2 (Boolean):  longitud del password del admin
- Flag3 (Time):     primer caracter del password (time-based)
- Flag4 (Error):    exfil completa del password (error-based)

> Nota: no incluyo payloads aquí para que el lab se use de forma responsable. En el momento de ejecutar docker compose up --build, si hay algun error relacionada con que no existe la carpeta static en la ruta sqli-lab-docker/web. La podeis crear vosotros mismos en ese directorio y volver a ejecutar docker compose up --build
