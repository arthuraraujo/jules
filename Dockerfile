# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install uv (the Rust-based Python package installer)
# We are using the standalone installer which is fast and simple.
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get remove -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add uv to the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Step 4: Copy the project files into the container
# We copy pyproject.toml first to leverage Docker layer caching.
COPY pyproject.toml ./
# Copy the application source code
COPY src/ ./src/

# Step 5: Install the Python dependencies using uv
# This reads pyproject.toml and installs the specified packages.
# We also need to copy the lock file if it exists
COPY uv.lock ./uv.lock
RUN uv pip sync pyproject.toml

# Step 6: Expose the port that Streamlit runs on
EXPOSE 8501

# Step 7: Add a healthcheck to verify the app is running
HEALTHCHECK --interval=15s --timeout=5s \
  CMD curl -f http://localhost:8501/_stcore/health

# Step 8: Define the command to run the application
# We use the full path to the streamlit executable to be explicit.
# The --server.runOnSave=false is a good practice for production.
# The --server.address=0.0.0.0 allows the app to be accessible from outside the container.
CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.runOnSave=false"]
