from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def image_to_story(img_path):
   
    image = Image.open(img_path).convert('RGB')
    
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    
    story = f"Once upon a time, {description}. The scene invites the reader to imagine the untold adventure that follows."
    return story

img_file = "random.jpg"
print(image_to_story(img_file))
