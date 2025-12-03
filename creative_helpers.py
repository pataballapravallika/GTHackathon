import os
import io
import zipfile
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

HF_MODEL_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

def generate_captions(product_name: str, n: int = 10):
    """
    Generates n short ad captions using Hugging Face Inference API.
    """
    captions = []
    for i in range(n):
        prompt = f"Write a short, catchy, modern advertisement caption for a product called '{product_name}'. Keep it under 12 words."
        payload = {"inputs": prompt, "options": {"wait_for_model": True}}
        try:
            response = requests.post(HF_MODEL_URL, headers=HF_HEADERS, json=payload, timeout=40)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and "generated_text" in data[0]:
                    caption = data[0]["generated_text"]
                elif isinstance(data, dict) and "generated_text" in data:
                    caption = data["generated_text"]
                else:
                    caption = str(data)
                captions.append(caption.strip().split("\n")[0])
            else:
                captions.append(f"{product_name} — premium quality!")
        except Exception:
            captions.append(f"{product_name} — amazing choice!")
    return captions

def generate_images_replicate(prompts):
    import replicate

    images = []

    for prompt in prompts:
        try:
            output_urls = replicate.run(
                "stability-ai/stable-diffusion-xl:latest",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024
                }
            )

            img_url = output_urls[0]
            img_data = requests.get(img_url, timeout=60).content
            img = Image.open(io.BytesIO(img_data)).convert("RGBA")
            images.append(img)

        except Exception as e:
            print("Error generating image:", e)

    return images


def overlay_logo_on_images(images, logo_bytes, ratio=0.18):
    """
    Overlays logo bottom-right on each image.
    ratio = size of logo relative to image width.
    """
    logo = Image.open(io.BytesIO(logo_bytes)).convert("RGBA")
    final_images = []
    for img in images:
        w, h = img.size
        logo_w = int(w * ratio)
        aspect_ratio = logo.width / logo.height
        logo_h = int(logo_w / aspect_ratio)
        logo_resized = logo.resize((logo_w, logo_h))
        canvas = img.copy()
        position = (w - logo_w - 20, h - logo_h - 20)
        canvas.paste(logo_resized, position, logo_resized)
        final_images.append(canvas)
    return final_images

def create_zip_bytes(images, captions, product_name="product"):
    """
    Creates ZIP file in memory containing images + captions and returns bytes.
    """
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for idx, img in enumerate(images, start=1):
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            zipf.writestr(f"{product_name}_{idx}.png", img_bytes.read())
        zipf.writestr("captions.txt", "\n".join(captions))
    memory_file.seek(0)
    return memory_file.getvalue()

def make_prompts(product_name: str, n=10):
    styles = [
        "minimal clean advertisement",
        "luxury premium gold theme",
        "colorful festival theme vibrant",
        "dark cinematic lighting commercial",
        "retro vintage poster style",
        "pastel soft ecommerce background",
        "street graffiti urban theme",
        "premium glossy magazine ad look",
        "nature outdoors fresh green background",
        "futuristic neon 3D rendered style"
    ]
    prompts = []
    for i in range(n):
        style = styles[i % len(styles)]
        prompts.append(f"High-quality advertisement creative for {product_name}, {style}, 4k resolution, photorealistic.")
    return prompts
