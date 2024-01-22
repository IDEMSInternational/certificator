from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from fastapi import HTTPException, FastAPI, status
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from certificator.certificates import make_certificate


class Settings(BaseSettings):
    font: str
    static_url_base: str = "http://localhost:8000/static/"
    storage_root: str = "storage"
    templates_root: str = "templates"


settings = Settings()
app = FastAPI()


@dataclass()
class Certificate:
    id: str
    image: bytes
    url: str = ""


class CertificateSpec(BaseModel):
    name: str
    template: str


@app.get("/")
def hello():
    return {"Hello": "World"}


@app.post("/certificates")
def create_certificate(spec: CertificateSpec):
    try:
        img = make_certificate(
            f"{settings.templates_root}/{spec.template}.png",
            settings.font,
            spec.name,
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Template not found",
        )

    cert = Certificate(
        id=sha1(f"{spec.template}_{spec.name}".encode()).hexdigest(),
        image=img,
    )
    save_certificate(cert)

    return {"id": cert.id, "url": cert.url}


@app.get("/templates")
def list_templates():
    return {"templates": [t.stem for t in Path(settings.templates_root).glob("*.png")]}


def save_certificate(cert):
    root = Path(settings.storage_root)
    root.mkdir(parents=True, exist_ok=True)

    filename = f"{cert.id}.png"

    with open(root / filename, "wb") as img:
        img.write(cert.image)

    cert.url = settings.static_url_base + filename

    return cert
