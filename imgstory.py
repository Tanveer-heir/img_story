from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import torch
import os
import random
import datetime
import csv

# Load Model/Processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def image_to_caption(img_path):
    image = Image.open(img_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)
    return description

def suggest_names(caption):
    names_pool = ["Alex", "Sam", "Jordan", "Riley", "Morgan", "Casey", "Charlie"]
    main = random.choice(names_pool)
    secondary = random.choice([n for n in names_pool if n != main])
    if any(x in caption.lower() for x in ["person", "man", "woman", "child"]):
        return main, secondary
    return main, None

def expand_caption(
    caption, 
    style="Fairy Tale", 
    main_name=None, 
    secondary_name=None, 
    length="short", 
    twist=None
):
    base = caption
    adventure_places = ["enchanted forest", "mysterious castle", "hidden valley"]
    sci_fi_places = ["starship", "alien planet", "space colony"]
    horror_places = ["abandoned mansion", "foggy graveyard", "deserted village"]
    fairytale_events = [
        "discovered a magical artifact",
        "met an unexpected companion",
        "faced a tricky riddle from the wise owl"
    ]
    detective_events = [
        "noticed a suspicious footprint near the scene",
        "received an anonymous tip about the crime",
        "analyzed a strange piece of evidence"
    ]
    sci_fi_events = [
        "encountered friendly robots",
        "found a portal to another dimension",
        "received a cryptic transmission from deep space"
    ]
    horror_events = [
        "heard footsteps echoing in the darkness",
        "found an old diary with chilling secrets",
        "saw shadows moving outside the window"
    ]

    # Insert character names
    if main_name:
        base = base.replace("person", main_name).replace("man", main_name).replace("woman", main_name)
        if secondary_name:
            base += f" and {secondary_name}"

    twist_text = f" Suddenly, {twist}." if twist else ""

    # Choose events and places
    if style == "Fairy Tale":
        place = random.choice(adventure_places)
        events = random.sample(fairytale_events, 2)
        story = (
            f"Once upon a time, {base} traveled into the {place}. {events[0].capitalize()}. "
            f"{events[1].capitalize()}. {twist_text} "
        )
        if length == "long":
            story += "After many challenges and magical encounters, they learned a lesson about bravery and kindness. "
            story += "As the sun set, their journey became a legend told for generations. "
        story += "The scene invites adventure and wonder."
        return story

    elif style == "Detective":
        place = "crime scene"
        events = random.sample(detective_events, 2)
        story = (
            f"{base} arrived at the {place}. {events[0].capitalize()}. {events[1].capitalize()}. {twist_text} "
        )
        if length == "long":
            story += f"After interviewing witnesses and investigating clues, {main_name or 'the detective'} cracked the mystery, revealing a clever twist no one saw coming. "
            story += "Justice was served, and the town felt safe again."
        story += "Inspector {main_name or 'Holmes'} finished the case."
        return story

    elif style == "Sci-Fi":
        place = random.choice(sci_fi_places)
        events = random.sample(sci_fi_events, 2)
        story = (
            f"In the far future, {base} explored the {place}. {events[0].capitalize()}. "
            f"{events[1].capitalize()}. {twist_text} "
        )
        if length == "long":
            story += "Facing alien challenges and interstellar adventures, they discovered secrets that changed humanity’s future. "
            story += "The universe became a little less mysterious after that journey."
        story += "The ship's computer beeped ominously."
        return story

    elif style == "Horror":
        place = random.choice(horror_places)
        events = random.sample(horror_events, 2)
        story = (
            f"It was a dark night at the {place} when {base} appeared. {events[0].capitalize()}. {events[1].capitalize()}. {twist_text} "
        )
        if length == "long":
            story += "Fear spread and survival became the only goal—until the dawn finally broke, bringing relief and new scars. "
            story += "This haunting tale echoed for years in local whispers."
        story += "Unseen eyes watched."
        return story

    elif style == "Summary":
        story = f"Image summary: {base}."
        if length == "long":
            story += f"\nIn detail: This image invites many interpretations, each shaped by the imagination and context of the viewer."
        return story

    # Default
    story = f"Once upon a time, {base}. {twist_text} The scene invites adventure and wonder."
    if length == "long":
        story += "Their experience grew richer and more dramatic as time passed."
    return story

def log_story(img_path, story, style):
    with open("story_log.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        writer.writerow([os.path.basename(img_path), style, now, story])

def browse_image():
    file_path = filedialog.askopenfilename(title="Select an Image", 
                                           filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
    img_path_var.set(file_path)
    story_text.delete(1.0, tk.END)
    caption_var.set("")

def generate_story():
    img_path = img_path_var.get()
    if not img_path or not os.path.exists(img_path):
        messagebox.showerror("Error", "Please select a valid image file!")
        return
    style = style_var.get()
    length = length_var.get()
    twist = twist_var.get()
    auto_char = char_name_var.get()
    caption = image_to_caption(img_path)
    caption_var.set(f"Caption: {caption}")
    main_name, secondary_name = (None, None)
    if auto_char:
        main_name, secondary_name = suggest_names(caption)
    story = expand_caption(
        caption, 
        style=style, 
        main_name=main_name, 
        secondary_name=secondary_name, 
        length=length, 
        twist=twist
    )
    story_text.delete(1.0, tk.END)
    story_text.insert(tk.END, story)
    log_story(img_path, story, style)
    messagebox.showinfo("Story Generated", "Story generated and logged to story_log.csv!")

def save_story():
    story = story_text.get(1.0, tk.END).strip()
    if not story:
        messagebox.showwarning("Warning", "No story to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt")],
                                             title="Save Story As")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(story)
        messagebox.showinfo("Saved", f"Story saved to {file_path}")

# GUI Setup
root = tk.Tk()
root.title("AI Image Story Generator")

img_path_var = tk.StringVar()
caption_var = tk.StringVar()

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky="NSEW")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Label(frame, text="Select Image:").grid(row=0, column=0, sticky="W")
ttk.Entry(frame, textvariable=img_path_var, width=40).grid(row=0, column=1, sticky="EW")
ttk.Button(frame, text="Browse", command=browse_image).grid(row=0, column=2, padx=4)

ttk.Label(frame, text="Story Style:").grid(row=1, column=0, sticky="W")
style_var = tk.StringVar(value="Fairy Tale")
style_option = ttk.Combobox(frame, textvariable=style_var, 
                            values=["Fairy Tale", "Detective", "Sci-Fi", "Horror", "Summary"])
style_option.grid(row=1, column=1, sticky="EW")

ttk.Label(frame, text="Story Length:").grid(row=2, column=0, sticky="W")
length_var = tk.StringVar(value="short")
length_option = ttk.Combobox(frame, textvariable=length_var, values=["short", "long"])
length_option.grid(row=2, column=1, sticky="EW")

ttk.Label(frame, text="Plot Twist (optional):").grid(row=3, column=0, sticky="W")
twist_var = tk.StringVar()
ttk.Entry(frame, textvariable=twist_var, width=40).grid(row=3, column=1, columnspan=2, sticky="EW")

char_name_var = tk.BooleanVar(value=True)
ttk.Checkbutton(frame, text="Auto add character names", variable=char_name_var).grid(row=4, column=0, columnspan=3, sticky="W")

ttk.Button(frame, text="Generate Story", command=generate_story).grid(row=5, column=0, columnspan=3, pady=8)

ttk.Label(frame, textvariable=caption_var, foreground="blue").grid(row=6, column=0, columnspan=3, sticky="W")

story_text = tk.Text(frame, height=10, width=60, wrap=tk.WORD)
story_text.grid(row=7, column=0, columnspan=3, pady=4, sticky="NSEW")

ttk.Button(frame, text="Save Story", command=save_story).grid(row=8, column=0, columnspan=3, pady=4)

frame.columnconfigure(1, weight=1)

root.mainloop()
