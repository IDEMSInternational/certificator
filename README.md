# Certificator

Create customisable award certificates.

# Quick start

Create a directory called 'fonts'. Obtain a font (OTF or TTF) and place it in the 'fonts' directory. Create a file called '.env' and add an entry that tells the app where to find your font - let's say your font is called 'your_font.ttf'.

```
FONT=fonts/your_font.ttf
```

Start the service.

```
docker compose up -d
```

Create a certificate using the example template.

```
http :8000/certificates name=Example template=grid
```

The response contains the location of the certificate.
```
{
    "url": "http://localhost:8080/4bcdb6e4403bc5476708bb4b80f1ed7c09b7bf3b.png",
    "id": "4bcdb6e4403bc5476708bb4b80f1ed7c09b7bf3b"
}
```

View API docs at http://localhost:8000/docs .

# Configuration

Certificator is configured via environment variables.

- `BOX`: Define an area in the template where the awardee's name will be placed. For example, `[0.1, 0.3, 0.6, 0.4]`, defines a box whose top-left point is 10% from the left border of the certificate template, and 30% from the top; the bottom-right point is 60% from left and 40% from top. Expressed as a 4-tuple of numbers, each with a value between 0 and 1. The first two numbers define the start (top-left) point, the last two the end (bottom-right) point. Default:`[0.072, 0.31, 0.596, 0.436]`.
- `COLOR`: Color to use for the awardee's name. Supports CCS3-style color specifiers e.g. `#ff0000`, `red`, etc. See [color names] in the documentation for the Pillow library for full details. Default: `#174168`.
- `FONT`: Local file path to OTF or TTF font to use for the awardee's name. No default, must be set.
- `STATIC_URL_BASE`: Base URL from which certificate images will be served as static assets. Default: `http://localhost:8000/static/`
- `STORAGE_ROOT`: Local file path where certificates will be saved. Default: `storage`.
- `TEMPLATES_ROOT`: Local file path where certificate templates will be read from. Default: `templates`.

# Templates

Certificate templates are PNG files. The example template (templates/grid.png) can be used as a basis for custom templates.

# Deployment

A Dockerfile and Docker Compose file are provided and can be used as a basis for your deployment.

# Development

```
# Create a virtual environment
python -m venv .venv

# Activate virtual environment - Linux / Mac
source .venv/bin/activate

# Activate virtual environment - Windows
.venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install the project in dev mode
pip install --editable '.[dev]'

# Create env file
echo "FONT=fonts/your_font.ttf" > .env

# Start the service
uvicorn --env-file=.env certificator.api:app --reload
```


[color names]: https://pillow.readthedocs.io/en/stable/reference/ImageColor.html#color-names
