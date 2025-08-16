## Agent Instructions for Face Generator App

This project is a Streamlit application that generates images based on user prompts.

### Project Structure
- `src/app.py`: The main Streamlit application file.
- `src/assets/`: Contains placeholder images for the generator.
- `pyproject.toml`: Manages project dependencies using `uv`.
- `Dockerfile`: For containerizing the application.
- `README.md`: Contains user-facing documentation.

### Development Workflow
1.  **Dependencies**: All Python dependencies are managed in `pyproject.toml`. Use `uv venv` to create a virtual environment and `uv pip install -e .` to install dependencies.
2.  **Running Locally**: Use `uv run streamlit run src/app.py` to run the application.
3.  **Image Generation**: The current image generation is a placeholder. It randomly selects images from `src/assets`. The goal is to build the full application structure so that a real model can be plugged in later.
4.  **Docker**: A `Dockerfile` is provided for building and running the application in a container. Use `docker build -t face-generator-app .` and `docker run -p 8501:8501 face-generator-app`.
5.  **UI/UX**: Keep the UI clean and intuitive. Use Streamlit's layout features to organize components logically.
