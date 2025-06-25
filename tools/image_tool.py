from langchain.tools import Tool
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class ImageAnalyzer:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").eval()

    def __call__(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(**inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption

image_tool = Tool(
    name="ImageAnalyzer",
    func=ImageAnalyzer(),
    description="Extracts a caption or text from an image file."
)
