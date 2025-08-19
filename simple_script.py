# simple_analyzer.py - SCRIPT QUI MARCHE DIRECT
import torch
from PIL import Image
from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
import fitz  # PyMuPDF
import io
import sys

def convert_pdf_to_image(pdf_path):
    """Convert PDF to PIL Image"""
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_data = pix.tobytes("ppm")
    image = Image.open(io.BytesIO(img_data))
    doc.close()
    return image

def analyze_drawing(image_path):
    """Analyze mechanical drawing - SIMPLE VERSION"""
    
    print(f"🔧 Loading model...")
    processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
    model = LlavaNextForConditionalGeneration.from_pretrained(
        "llava-hf/llava-v1.6-mistral-7b-hf",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    print(f"📄 Processing image: {image_path}")
    
    # Load image
    if image_path.endswith('.pdf'):
        image = convert_pdf_to_image(image_path)
    else:
        image = Image.open(image_path)
    
    # Simple prompt that works
    prompt = "What dimensions and tolerances can you see in this mechanical drawing? List them all."
    
    # Process
    inputs = processor(prompt, image, return_tensors="pt").to(model.device)
    
    print(f"🔍 Running analysis...")
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=512, do_sample=False)
    
    # Get result
    response = processor.decode(output[0], skip_special_tokens=True)
    
    # Clean up response
    if prompt in response:
        response = response.split(prompt)[-1].strip()
    
    return response

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python simple_analyzer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = analyze_drawing(image_path)
    
    print("\n" + "="*60)
    print("RESULTAT:")
    print("="*60)
    print(result)
    print("="*60)