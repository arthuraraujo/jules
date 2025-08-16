# 👤 AI Persona Generator

This project is a Streamlit web application that generates images from text prompts using the **Stable Diffusion** model. It's designed with a clean user interface and can be run both locally and as a Docker container.

## ✨ Features

-   **AI-Powered Image Generation:** Utilizes the `runwayml/stable-diffusion-v1-5` model to generate high-quality images from text.
-   **Interactive UI:** A clean and user-friendly interface built with Streamlit.
-   **Advanced Controls:**
    -   **Negative Prompts:** Specify what you *don't* want to see in the generated image.
    -   **Image Count:** Choose how many images to generate at once.
-   **Image Download:** Easily download your favorite creations with a single click.
-   **`uv` Powered:** Uses `uv` for fast and reliable dependency and environment management.
-   **Dockerized:** Includes a `Dockerfile` for easy containerization and deployment.

## 🧠 The Model

This application uses the `runwayml/stable-diffusion-v1-5` model from the Hugging Face Hub.

**Important:** The first time you run the application, it will download the model, which is several gigabytes in size. This may take some time depending on your internet connection. The model is then cached for subsequent runs.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   `uv` – a fast Python package installer. If you don't have it, you can install it with:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
-   [Docker](https://www.docker.com/get-started) (for running with Docker)
-   For GPU acceleration, you'll need an NVIDIA GPU with CUDA installed. The app will automatically fall back to CPU if a GPU is not available.

### 1. Running Locally with `uv`

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and install dependencies:**
    First, create the virtual environment:
    ```bash
    uv venv
    ```
    Then, sync the dependencies:
    ```bash
    uv pip sync pyproject.toml
    ```

3.  **Run the Streamlit application:**
    ```bash
    uv run streamlit run src/app.py
    ```

    The application should now be running and accessible at `http://localhost:8501`.

### 2. Running with Docker

1.  **Build the Docker image:**
    From the root of the project directory, run the following command to build the image:
    ```bash
    docker build -t ai-persona-generator .
    ```

2.  **Run the Docker container:**
    After the image is built, run it with:
    ```bash
    docker run -p 8501:8501 ai-persona-generator
    ```
    To enable GPU access inside the container (requires NVIDIA Container Toolkit), use:
    ```bash
    docker run --gpus all -p 8501:8501 ai-persona-generator
    ```

    The application will be accessible in your browser at `http://localhost:8501`.
