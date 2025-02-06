"""Vector quantization model implementation."""
from typing import Tuple, Optional
import torch
from torch import nn
from vector_quantize_pytorch import VectorQuantize
from transformers import BartForConditionalGeneration, BartTokenizer
from sentence_transformers import SentenceTransformer

class DecisionVQVAE(nn.Module):
    """Vector quantization model for decision making."""
    
    def __init__(
        self, 
        input_dim: int = 768,
        codebook_dim: int = 256,
        codebook_size: int = 512,
        embedding_model: str = "all-MiniLM-L6-v2",
        bart_model: str = "facebook/bart-base"
    ):
        """Initialize VQ model.
        
        Args:
            input_dim: Input embedding dimension
            codebook_dim: VQ codebook dimension
            codebook_size: Number of codes in codebook
            embedding_model: Name of sentence embedding model
            bart_model: Name of BART model for decoding
        """
        super().__init__()
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Encoder network
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 512),
            nn.ReLU(),
            nn.Linear(512, codebook_dim)
        )
        
        # Vector quantizer
        self.vq = VectorQuantize(
            dim=codebook_dim,
            codebook_size=codebook_size,
            decay=0.8,
            commitment_weight=1.0
        )
        
        # Decoder network
        self.decoder = nn.Sequential(
            nn.Linear(codebook_dim, 512),
            nn.ReLU(),
            nn.Linear(512, input_dim)
        )
        
        # BART decoder
        self.bart_decoder = BartActionDecoder(bart_model)

    def encode_text(self, text: str) -> torch.Tensor:
        """Encode text using sentence transformer."""
        return torch.tensor(self.embedding_model.encode(text))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Forward pass through the model.
        
        Args:
            x: Input tensor
            
        Returns:
            Tuple of (reconstructed tensor, quantization indices, commitment loss)
        """
        z = self.encoder(x)
        quantized, indices, commit_loss = self.vq(z)
        recon = self.decoder(quantized)
        return recon, indices, commit_loss

    def decode_action(self, indices: torch.Tensor, context: str) -> str:
        """Decode quantization indices into action string."""
        return self.bart_decoder.decode_action(indices, context)


class BartActionDecoder:
    """BART-based decoder for converting codes to actions."""
    
    def __init__(self, model_name: str):
        """Initialize BART decoder.
        
        Args:
            model_name: Name of pretrained BART model
        """
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
    
    def decode_action(self, indices: torch.Tensor, context: str) -> str:
        """Decode indices into action string.
        
        Args:
            indices: Quantization indices
            context: Context string for generation
            
        Returns:
            Generated action string
        """
        input_text = f"Context: {context} | Codes: {indices.tolist()}"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        
        output = self.model.generate(
            inputs.input_ids, 
            max_length=128,
            num_beams=4,
            early_stopping=True
        )
        
        return self.tokenizer.decode(output[0], skip_special_tokens=True) 