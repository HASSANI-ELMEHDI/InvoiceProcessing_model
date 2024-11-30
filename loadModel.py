from transformers import DonutProcessor, VisionEncoderDecoderModel
DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2").save_pretrained("./models/donut-base-finetuned-cord-v2")
VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2").save_pretrained("./models/donut-base-finetuned-cord-v2")
