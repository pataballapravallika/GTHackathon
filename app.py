import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from creative_helpers import (
    generate_images_replicate,
    generate_captions,
    overlay_logo_on_images,
    create_zip_bytes,
    make_prompts
)

st.set_page_config(page_title="AI Creative Studio", layout="wide")
st.title("🎨 AI Creative Studio — Auto Creative Engine (Replicate + HF)")

product_name = st.text_input("Product Name", "My Product")
n = st.slider("Number of creatives", 4, 12, 10)

col1, col2 = st.columns(2)
with col1:
    prod_file = st.file_uploader("Upload product image", type=["png","jpg","jpeg"])
with col2:
    logo_file = st.file_uploader("Upload brand logo (PNG recommended)", type=["png","jpg","jpeg"])

if st.button("Generate"):
    if not prod_file or not logo_file:
        st.error("Please upload both product image and logo.")
    else:
        prompts = make_prompts(product_name, n)
        st.info("Generating images (Replicate SDXL)...")
        images = generate_images_replicate(prompts)

        st.info("Applying brand logo...")
        logo_bytes = logo_file.read()
        images_with_logo = overlay_logo_on_images(images, logo_bytes)

        st.info("Generating captions (HuggingFace)...")
        captions = generate_captions(product_name, n)

        st.success("Done — previews below")
        cols = st.columns(min(4, n))
        for i, img in enumerate(images_with_logo):
            with cols[i % len(cols)]:
                st.image(img, caption=captions[i] if i < len(captions) else f"Creative #{i+1}", use_column_width=True)

        zip_bytes = create_zip_bytes(images_with_logo, captions, product_name.replace(" ", "_"))
        st.download_button("⬇️ Download creatives ZIP", data=zip_bytes, file_name=f"{product_name}_creatives.zip", mime="application/zip")
