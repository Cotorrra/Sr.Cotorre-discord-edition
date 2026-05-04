FROM ghcr.io/astral-sh/uv:python3.14-alpine

COPY . /app
WORKDIR /app

ENV UV_NO_DEV=1
RUN uv sync --locked --no-install-project

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "bot.py"]