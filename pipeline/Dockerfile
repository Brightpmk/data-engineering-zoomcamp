FROM python:3.13.7-slim

# 1. Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# 2. Set the working directory FIRST
WORKDIR /code

# 3. Copy dependencies into the working directory
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# 4. Sync dependencies (this creates /code/.venv)
RUN uv sync --locked

# 5. Correctly update the PATH to look inside /code/.venv
ENV PATH="/code/.venv/bin:$PATH"

# 6. Copy your script
COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]