FROM ghcr.io/astral-sh/uv:0.10.0 AS uv
FROM python:3.14-slim

COPY --from=uv /uv /uvx /bin/
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
EXPOSE 8000
