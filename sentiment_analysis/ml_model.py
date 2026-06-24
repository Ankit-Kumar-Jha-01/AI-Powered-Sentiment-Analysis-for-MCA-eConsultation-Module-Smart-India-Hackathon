# # import os
# # import torch
# # from transformers import AutoTokenizer, AutoModelForSequenceClassification

# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "final_model")

# # tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
# # model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
# # model.eval()

# from transformers import AutoTokenizer, AutoModelForSequenceClassification

# MODEL_NAME = "ankitjha/student-sentiment-model"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# model.eval()


# LABEL_MAP = {
#     0: "negative",
#     1: "neutral",
#     2: "positive"
# }

# def predict_sentiment(text):
#     inputs = tokenizer(
#         text,
#         return_tensors="pt",
#         truncation=True,
#         padding=True
#     )

#     with torch.no_grad():
#         outputs = model(**inputs)

#     predicted_class = torch.argmax(outputs.logits, dim=1).item()
#     return LABEL_MAP[predicted_class]


import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "ankitjha07/Sentiment-analysis-MCAeCounsultation"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

LABEL_MAP = {
    0: "negative",
    1: "neutral",
    2: "positive"
}

def predict_sentiment(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predicted_class = torch.argmax(outputs.logits, dim=1).item()
    return LABEL_MAP[predicted_class]