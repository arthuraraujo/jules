import streamlit as st
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import io

# --- CONFIGURATION ---
MODEL_ID = "runwayml/stable-diffusion-v1-5"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# --- MODEL LOADING ---
@st.cache_resource
def load_pipeline():
    """Loads the diffusion pipeline and caches it."""
    try:
        pipe = DiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
        pipe = pipe.to(DEVICE)
        return pipe
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.error("This can happen if you are running out of memory. Try restarting the app or using a smaller model.")
        return None

# --- IMAGE GENERATION LOGIC ---
def generate_images(prompt: str, negative_prompt: str, num_images: int, pipe) -> list[Image.Image]:
    """Generates images using the Stable Diffusion pipeline."""
    if pipe is None:
        return []

    try:
        # For GPU, we can process images in batches. For CPU, it's safer one by one.
        if DEVICE == "cuda":
            images = pipe(prompt, negative_prompt=negative_prompt, num_images=num_images).images
        else:
            # Generate images one by one on CPU to avoid memory issues
            images = [pipe(prompt, negative_prompt=negative_prompt).images[0] for _ in range(num_images)]
        return images
    except Exception as e:
        st.error(f"An error occurred during image generation: {e}")
        return []


# --- UI SETUP ---
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="AI Persona Generator",
        page_icon="👤",
        layout="wide",
    )

    # --- Load Model ---
    pipe = load_pipeline()

    # --- Sidebar for controls ---
    with st.sidebar:
        st.title("👤 AI Persona Generator")
        st.markdown(
            "This app uses the **Stable Diffusion** model to generate images from text prompts."
            " Describe the scene you want to create, and the AI will bring it to life."
        )

        st.header("Generation Settings")
        prompt_text = st.text_area(
            "**Prompt** (What you want to see)",
            "A portrait of a person with cybernetic enhancements, in a neon-lit alley, detailed, science fiction.",
            height=100,
        )
        negative_prompt_text = st.text_area(
            "**Negative Prompt** (What you want to avoid)",
            "ugly, blurry, deformed, noisy, disfigured, watermark, text",
            height=100,
        )
        num_images = st.slider("Number of images to generate:", 1, 4, 1)

        generate_button = st.button("Generate Images", type="primary", disabled=(pipe is None))

    # --- Main content area ---
    st.header("Generated Images")

    if generate_button:
        if not prompt_text:
            st.warning("Please enter a prompt to generate images.")
        else:
            with st.spinner(f"Generating {num_images} image(s)... this may take a moment."):
                generated_images = generate_images(prompt_text, negative_prompt_text, num_images, pipe)

                if generated_images:
                    cols = st.columns(num_images)
                    for i, image in enumerate(generated_images):
                        with cols[i]:
                            st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)

                            # Create a byte buffer for the image
                            buf = io.BytesIO()
                            image.save(buf, format="PNG")
                            byte_im = buf.getvalue()

                            st.download_button(
                                label="Download Image",
                                data=byte_im,
                                file_name=f"generated_image_{i+1}.png",
                                mime="image/png",
                            )
    else:
        st.markdown("Your generated images will appear below.")


if __name__ == "__main__":
    main()
