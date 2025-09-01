FROM ghcr.io/astral-sh/uv:python3.9-bookworm-slim

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y libsndfile1 ffmpeg --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

COPY uv.lock /app/
COPY pyproject.toml /app/
# Install the project's dependencies using the lockfile and settings
RUN uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

CMD [ "uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0", "main:app" ]
