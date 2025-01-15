import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from sklearn.model_selection import train_test_split

# Lista de palavras e emojis
word_to_emoji = {
    "happy": "😊",
    "love": "❤️",
    "cat": "🐱",
    "dog": "🐶",
    "pizza": "🍕",
    "sun": "☀️",
    "moon": "🌙",
    "star": "⭐",
    "flower": "🌸",
    "tree": "🌳"
}

# Criando um dataset de palavras e emojis
data = [{"word": word, "emoji": emoji} for word, emoji in word_to_emoji.items()]

# Criando o dataset
dataset = Dataset.from_dict({
    "word": [item["word"] for item in data],
    "emoji": [item["emoji"] for item in data]
})

# Dividir em treinamento e validação
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)
train_dataset = Dataset.from_dict({
    "word": [item["word"] for item in train_data],
    "emoji": [item["emoji"] for item in train_data]
})
val_dataset = Dataset.from_dict({
    "word": [item["word"] for item in val_data],
    "emoji": [item["emoji"] for item in val_data]
})

# Carregar o tokenizer do DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

# Função de pré-processamento
def preprocess_function(examples):
    return tokenizer(examples["word"], padding="max_length", truncation=True, max_length=32)

# Aplicar o pré-processamento nos datasets
train_dataset = train_dataset.map(preprocess_function, batched=True)
val_dataset = val_dataset.map(preprocess_function, batched=True)

# Converter emojis para índices numéricos (como classificação)
emoji_list = list(word_to_emoji.values())
emoji_to_id = {emoji: idx for idx, emoji in enumerate(emoji_list)}

def encode_labels(examples):
    examples["label"] = [emoji_to_id[emoji] for emoji in examples["emoji"]]
    return examples

train_dataset = train_dataset.map(encode_labels, batched=True)
val_dataset = val_dataset.map(encode_labels, batched=True)

# Carregar o modelo DistilBERT para classificação de sequência
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=len(emoji_list))

# Definir argumentos de treinamento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01
)

# Inicializar o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# Treinar o modelo
trainer.train()

# Avaliar o modelo
results = trainer.evaluate()
print(results)

# Testar o modelo com novas palavras
def predict(word):
    inputs = tokenizer(word, return_tensors="pt", padding=True, truncation=True, max_length=32)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = torch.argmax(logits, dim=-1).item()
        return emoji_list[predicted_class_idx]

# Exemplo de predição

word = input("Digite...")

predicted_emoji = predict(word)
print(f"A palavra '{word}' foi associada ao emoji: {predicted_emoji}")
