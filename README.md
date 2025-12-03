# GTHackathon
# AI Creative Studio — Auto Creative Engine  
Generate 10+ high-quality ad creatives + captions automatically using Generative AI (SDXL + HuggingFace).

## 🚀 Project Overview
Businesses spend weeks designing multiple ad creatives for different campaigns.  
**AI Creative Studio** automates this entire workflow:

- Upload a **product image**
- Upload a **brand logo**
- AI generates **10+ high-resolution ad creatives**
- AI writes **captions** for each ad
- Download everything as a **ZIP file**

This project was built for the **GroundTruth Mini AI Hackathon** under the challenge:  
**H-003 | The AI Creative Studio (Generative AI & MarTech).**

---

## ✨ Features
- ✔ **Stable Diffusion XL (SDXL)** via Replicate for image generation  
- ✔ Automatic prompt generation (10 creative styles)  
- ✔ Logo overlay on generated images  
- ✔ **HuggingFace Inference API** for caption generation  
- ✔ Streamlit UI for smooth user experience  
- ✔ Downloadable ZIP containing:  
  - High-res creatives (PNG)  
  - Captions file  

---

## 🏗️ Tech Stack
| Component      | Technology Used |
|----------------|-----------------|
| UI Framework   | Streamlit |
| Image Generation | Stable Diffusion XL (via Replicate API) |
| Text Generation | HuggingFace GPT-2 (or replaceable model) |
| Backend | Python |
| Packaging | ZIP export |
| Environment | .env for API keys |

---

## 🧠 Architecture
            ┌──────────────────────────┐
            │      Streamlit UI        │
            │ Upload product + logo    │
            └─────────────┬────────────┘
                          │
            ┌─────────────▼────────────┐
            │     app.py (Main App)    │
            └─────────────┬────────────┘
                          │
    ┌─────────────────────┴─────────────────────┐
    │                 creative_helpers.py        │
    │                                             │
    │ • make_prompts()                            │
    │ • generate_images_replicate() → SDXL API    │
    │ • overlay_logo_on_images()                  │
    │ • generate_captions() → HuggingFace API     │
    │ • create_zip_bytes()                        │
    └─────────────────────┬─────────────────────┘
                          │
            ┌─────────────▼──────────────┐
            │        Output ZIP          │
            │ creatives + captions.txt   │
            └────────────────────────────┘

---

## 📂 Folder Structure

GTHackathon/
│── app.py
│── creative_helpers.py
│── requirements.txt
│── .env 
│── venv/ 
│── README.md



---

## 🔧 Installation & Setup

### 1️⃣ Clone repo

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

### Create virtual environment

   python -m venv venv
   venv\Scripts\activate      # Windows


 ### 3️⃣ Install dependencies
     pip install -r requirements.txt


### 4️⃣ Add API keys

   REPLICATE_API_TOKEN=your_replicate_token
   HUGGINGFACE_API_TOKEN=your_huggingface_token

## Run the App

   streamlit run app.py

