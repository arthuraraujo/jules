import streamlit as st
import random
from pathlib import Path
from PIL import Image

# --- PATH SETTINGS ---
CURRENT_DIR = Path(__file__).parent
ASSETS_DIR = CURRENT_DIR / "assets"
IMAGE_FILES = list(ASSETS_DIR.glob("*.jpg"))


# --- IMAGE GENERATION LOGIC (PLACEHOLDER) ---
def generate_images(prompt: str, num_images: int) -> list[Image.Image]:
    """
    Simulates image generation based on a prompt.
    Instead of a real model, it randomly selects from placeholder images.
    """
    if not IMAGE_FILES:
        st.error("No placeholder images found in the 'assets' directory. Please add some.")
        return []

    selected_images = random.choices(IMAGE_FILES, k=num_images)
    images = [Image.open(img_path) for img_path in selected_images]
    return images


# --- UI SETUP ---
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="AI Persona Generator",
        page_icon="👤",
        layout="wide",
    )

    # --- Sidebar for controls ---
    with st.sidebar:
        st.title("👤 AI Persona Generator")
        st.markdown(
            "This app uses a placeholder to simulate generating images of a specific person."
            " In a real-world scenario, this would be powered by a fine-tuned AI model."
        )

        st.header("Generation Settings")
        prompt_text = st.text_area(
            "Enter your prompt:",
            "A person standing in front of a futuristic cityscape at night, neon lights reflecting on their face.",
            height=150,
        )
        num_images = st.slider("Number of images to generate:", 1, 3, 1)

        generate_button = st.button("Generate Images", type="primary")

    # --- Main content area ---
    st.header("Generated Images")
    st.markdown("Your generated images will appear below.")

    if generate_button:
        if not prompt_text:
            st.warning("Please enter a prompt to generate images.")
        else:
            with st.spinner(f"Generating {num_images} image(s) based on your prompt..."):
                generated_images = generate_images(prompt_text, num_images)

                if generated_images:
                    cols = st.columns(num_images)
                    for i, image in enumerate(generated_images):
                        with cols[i]:
                            st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)


if __name__ == "__main__":
    main()
