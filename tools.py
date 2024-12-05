from transformers import AutoModel, AutoTokenizer
from torch import nn

class Vectorizer(nn.Module):

    def __init__(self, model="albert/albert-base-v2"):

        super().__init__()

        self.model = AutoModel.from_pretrained(model, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)


    def forward(self, text):
        tokenized_input = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        # move to cuda
        for key in tokenized_input:
            tokenized_input[key] = tokenized_input[key].to(self.device)
        return self.model(**tokenized_input).last_hidden_state[:, 0, :]
    @property
    def device(self):
        return self.model.device
    
    @property
    def dim(self):
        return self.model.config.hidden_size
