# 🖼️ AI Image Story Generator

An intelligent desktop application that **creates imaginative stories from images** using **Salesforce BLIP (Bootstrapped Language Image Pretraining)**.  
The tool generates captions for images and expands them into creative narratives across multiple genres — Fairy Tale, Detective, Sci-Fi, Horror, and Summary.

---

## ✨ Features

- 🧠 **Automatic Image Captioning** using the BLIP Transformer model  
- 📜 **Story Generation** with selectable writing styles and length  
- 🧑‍🤝‍🧑 **Auto Character Name Suggestion** based on image content  
- 🔄 **Custom Plot Twists** for unique storytelling  
- 💾 **Story Logging & Saving** — every generated story is saved in `story_log.csv` and can be exported as a `.txt` file  
- 🪟 **Simple GUI** built using Python’s `tkinter`  

---

## 🧩 Tech Stack

- **Python 3.8+**  
- **Transformers** (`Salesforce/blip-image-captioning-base`)  
- **PyTorch**  
- **Pillow (PIL)**  
- **Tkinter (GUI)**  

---

## 🚀 Usage

### 1. Run the application

### 2. How to use
- Click **"Browse"** to select an image.  
- Choose the **story style** (Fairy Tale, Detective, Sci-Fi, Horror, or Summary).  
- Optionally add a **plot twist** or toggle **auto character naming**.  
- Click **"Generate Story"** to create a narrative.  
- The story appears in the text box and is automatically logged to `story_log.csv`.  
- Use **"Save Story"** to export your story as a `.txt` file.

---

## 🧠 How It Works

1. **Caption Generation**  
   - The selected image is processed using `BlipProcessor` and `BlipForConditionalGeneration`.  
   - The model describes the image in natural language.

2. **Story Expansion**  
   - The caption is transformed into a short or long narrative using template-based storytelling logic.  
   - Users can apply genres and add creative twists.

3. **Story Logging**  
   - Each story, along with the image filename, style, timestamp, and text, is saved into `story_log.csv`.

---

## 📁 Log Format (`story_log.csv`)
| Image File | Style | Date-Time | Story |
|-------------|--------|------------|--------|
| photo.jpg | Fairy Tale | 2025-10-23 21:40 | Once upon a time, Alex traveled into the enchanted forest... |

---

## 🧑‍💻 Example Output

**Input:**  
An image of a person standing near a castle under the moon.  

**Generated Story (Fairy Tale, long):**
> Once upon a time, Alex traveled into the enchanted forest. They discovered a magical artifact. Met an unexpected companion. After many challenges and magical encounters, they learned a lesson about bravery and kindness. As the sun set, their journey became a legend told for generations. The scene invites adventure and wonder.


---

## 🧠 Model Reference
**BLIP: Bootstrapped Language-Image Pretraining**  
Model: `Salesforce/blip-image-captioning-base`  
It performs image caption generation and text-conditioned visual understanding tasks efficiently.

---

## 🛡️ License
This project is licensed under the **MIT License**.

---

## 👨‍💻 Author
Developed by Tanveer Singh - 2025  
Inspired by the potential of AI creativity through vision-language models.

---




