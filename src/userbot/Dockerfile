FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:0.8.11 /uv /uvx /bin/

WORKDIR /app

ENV UV_LINK_MODE=copy

# Install build tools required for packages like tgcrypto
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libffi-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies via UV
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --group userbot --no-install-project

# Copy only necessary files for migrations
COPY core/ ./core/
COPY src/userbot/ ./src/userbot/
COPY src/models/ ./src/models/

CMD ["uv", "run", "python", "-m", "src.userbot.main"]