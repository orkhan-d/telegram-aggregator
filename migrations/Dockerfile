FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/

WORKDIR /app

ENV UV_LINK_MODE=copy

# Install dependencies via UV
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --group migrations --no-install-project

# Copy only necessary files for migrations
COPY alembic.ini ./alembic.ini
COPY migrations/ ./migrations/
COPY core/ ./core/
COPY src/models/ ./src/models/

CMD ["uv", "run", "alembic", "upgrade", "head"]