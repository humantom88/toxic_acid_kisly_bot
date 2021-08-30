import torch

from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)

if torch.cuda.is_available():
    model.cuda()

class Analyzer:
    def __init__(self, model):
        self.model = model

    def text2toxicity(self, text, aggregate=True):
        """ Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""
        with torch.no_grad():
            inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
            proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
        if isinstance(text, str):
            proba = proba[0]
        if aggregate:
            return 1 - proba.T[0] * (1 - proba.T[-1])
        return proba
    
    def answer_message(self, message):
        if message == None or message == '':
            return "Ты отправил пустое сообщение"
        result = self.text2toxicity(message)

        if result == None:
            return "Не удалось обработать сообщение"

        toxicity = "%.2f" % (result * 100)

        if result >= 0.9:
            return f"За тобой уже выехали! (Токсичность: {toxicity}) %" 
        if result >= 0.8:
            return f"Это непростительно! (Токсичность: {toxicity}) %" 
        if result >= 0.7:
            return f"Да ты прям токсик! (Токсичность: {toxicity}) %" 
        if result >= 0.6:
            return f"Ходишь по краю, детка... (Токсичность: {toxicity}) %" 
        else:
            return f"Вроде норм, '{message}' не токсично. (Токсичность: {toxicity}) %"

# analyzer = Analyzer(model)
# import pickle

# with open('analyzer.pkl', 'wb') as f:
#     pickle.dump(analyzer, f)