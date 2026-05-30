# DOCX to PDF API

A small FastAPI service that converts uploaded `.docx` files into `.pdf` files using LibreOffice in a Docker container.

## What it does

- Accepts a DOCX file on `POST /convert`
- Saves the upload to a temporary working directory
- Uses `soffice` in headless mode to generate a PDF
- Returns the PDF inline as the HTTP response
- Exposes a simple health endpoint at `GET /`

## Why this exists

This project is useful when you need consistent server-side DOCX to PDF conversion without depending on Microsoft Word or manual desktop tooling.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- LibreOffice headless
- Docker

## API

### `GET /`

Returns:

```json
{ "ok": true }
```

### `POST /convert`

Upload a DOCX file as multipart form data with the field name `file`.

Example:

```bash
curl -X POST "http://localhost:8080/convert" \
  -F "file=@example.docx" \
  --output converted.pdf
```

## Run with Docker

1. Build the image:

```bash
docker build -t docx-to-pdf .
```

2. Run the container:

```bash
docker run --rm -p 8080:8080 docx-to-pdf
```

3. Test the service:

```bash
curl http://localhost:8080/
```

## Project Layout

- `main.py` - FastAPI app and conversion endpoint
- `dockerfile` - Container image for the service
- `docker-compose.yml` - Compose configuration for deployment
- `requirements.txt` - Python dependencies
- `fonts/` - Optional custom fonts for conversion
- `temp/` - Runtime temporary files

## Fonts and Temp Files

The repository is configured to ignore runtime temp files and bundled font binaries. If you want custom fonts inside the container, place them in `fonts/`.

The `fonts/fonts should be here.txt` file is a marker that explains where custom fonts belong without committing the actual font files.
 

 

