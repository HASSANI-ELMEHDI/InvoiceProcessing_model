from PIL import Image
import os
import re
import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from torch.quantization import quantize_dynamic

# Paths to local model and processor
MODEL_PATH = "./models/donut-base-finetuned-cord-v2"

# Ensure the local model directory exists
if not os.path.exists(MODEL_PATH):
    print("Downloading model locally...")
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
    processor.save_pretrained(MODEL_PATH)
    model.save_pretrained(MODEL_PATH)
else:
    processor = DonutProcessor.from_pretrained(MODEL_PATH)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL_PATH)

# Quantize the model for faster inference
print("Quantizing the model...")
model = quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)

# Check and set the device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def process_image(image_path):
    """
    Generate data for an image using a pretrained Donut model.

    Args:
        image_path (str): Path to the input image file.

    Returns:
        Json format
    """

    # Check and set the device (CPU or GPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # Open the input image
    image = Image.open(image_path)


    # Prepare encoder inputs
    pixel_values = processor(image, return_tensors="pt").pixel_values

    # Prepare decoder inputs
    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

    # Generate answer
    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )

    # Postprocess the generated sequence
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()  # Remove the first task start token

    return processor.token2json(sequence)
