import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

LABELS = ["Entertainment", "Business", "Technology", "Health"]

class InputData(BaseModel):
    text: str

class BatchInputData(BaseModel):
    texts: List[str]

def load_keras_model(model_path: str):
    """Load and return the trained Keras model."""
    return load_model(model_path)

def load_tokenizer(tokenizer_path: str):
    """Load and return the tokenizer."""
    with open(tokenizer_path, "rb") as f:
        return pickle.load(f)

def preprocess_text(tokenizer_path: str, text_list: List[str]):
    """Tokenize and pad input text."""
    tokenizer = load_tokenizer(tokenizer_path)
    sequences = tokenizer.texts_to_sequences(text_list)
    return pad_sequences(sequences, maxlen=50, padding="post", truncating="post")

app = FastAPI()
model = load_keras_model("models/best_bilstm_model.h5")

@app.post("/predict")
def predict(data: InputData):
    """Predict using the loaded model and return label."""
    try:
        processed_text = preprocess_text("models/tokenizer.pkl", [data.text])
        prediction = model.predict(processed_text)[0]  
        predicted_label_index = prediction.argmax()  
        predicted_label = LABELS[predicted_label_index]

        return {
            "text": data.text,
            "prediction": prediction.tolist(),
            "label": predicted_label
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/batch-predict")
def batch_predict(data: BatchInputData):
    """Predict for multiple inputs."""
    try:
        processed_texts = preprocess_text("models/tokenizer.pkl", data.texts)
        predictions = model.predict(processed_texts)
        labels = [LABELS[p.argmax()] for p in predictions]

        return {
            "texts": data.texts,
            "predictions": predictions.tolist(),
            "labels": labels
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/model-info")
def model_info():
    """Return model metadata."""
    return {
        "model_name": "Headline Classifier",
        "version": "1.0.0",
        "trained_on": "2025-02-24",
        "accuracy": 0.97
    }
