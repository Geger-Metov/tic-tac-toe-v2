FROM python:3.12-slim

# Копируем бинарник uv из официального distroless-образа Astral
COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app/.venv

# Зависимости ставим отдельным слоем, до копирования кода приложения —
# слой пересобирается только когда меняются pyproject.toml/uv.lock,
# а не при каждой правке src/.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY src/tic_tac_toe ./tic_tac_toe/

# Кладём venv/bin в PATH, чтобы не писать "uv run" перед каждой командой
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "tic_tac_toe.main:app", "--host", "0.0.0.0", "--port", "8000"]
