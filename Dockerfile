FROM python:3.11-bookworm AS builder
WORKDIR /work
RUN pip install --upgrade build
COPY . .
RUN python -m build

FROM python:3.11-slim-bookworm
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1
EXPOSE 8000
WORKDIR /opt/idems/certificator
COPY --from=builder /work/dist/*.whl .
RUN pip install uvicorn *.whl
CMD ["uvicorn", "certificator.api:app", "--host", "0.0.0.0", "--port", "8000"]
