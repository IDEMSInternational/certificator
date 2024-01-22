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

# Start the service
FONT=fonts/your_font.ttf uvicorn certificator.api:app --reload
```
