import torch
from torch import nn
from vector_quantize_pytorch import VectorQuantize
from transformers import BartForConditionalGeneration, BartTokenizer
from sentence_transformers import SentenceTransformer  # 添加本地embedding模型

class DecisionVQVAE(nn.Module):
    def __init__(self, input_dim=768, codebook_dim=256, codebook_size=512):
        super().__init__()
        # 使用本地embedding模型
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, codebook_dim)
        )
        self.vq = VectorQuantize(
            dim=codebook_dim,
            codebook_size=codebook_size,
            decay=0.8,
            commitment_weight=1.0
        )
        self.decoder = nn.Sequential(
            nn.Linear(codebook_dim, 512),
            nn.ReLU(),
            nn.Linear(512, input_dim)
        )

    def encode_text(self, text: str) -> torch.Tensor:
        """使用本地模型进行文本编码"""
        return torch.tensor(self.embedding_model.encode(text))

    def forward(self, x):
        z = self.encoder(x)
        quantized, indices, commit_loss = self.vq(z)
        recon = self.decoder(quantized)
        return recon, indices, commit_loss

class BartActionDecoder:
    def __init__(self, model_name="facebook/bart-base"):
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
    
    def decode_action(self, indices: torch.Tensor, context: str) -> dict:
        input_text = f"Context: {context} | Codes: {indices.tolist()}"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        output = self.model.generate(
            inputs.input_ids, 
            max_length=128,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

class StructuredBartDecoder(nn.Module):
    def __init__(self, model_name="facebook/bart-base"):
        super().__init__()
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.bart = BartForConditionalGeneration.from_pretrained(model_name)
        self.action_embeddings = nn.Parameter(torch.randn(100, 768))  # 预定义动作嵌入
        
    def forward(self, context: str):
        # 上下文编码
        context_emb = self.embedding_model.encode(context)
        
        # 结构化注意力
        action_scores = torch.matmul(context_emb, self.action_embeddings.T)
        action_probs = torch.softmax(action_scores, dim=-1)
        
        # 条件生成
        return self.bart.generate(
            encoder_hidden_states=action_probs @ self.action_embeddings
        ) 