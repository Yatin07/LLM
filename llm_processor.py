"""
LLM Processing Module
Handles LLM-based query processing and response generation.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

logger = logging.getLogger(__name__)

class LLMProcessor:
    """Process queries using Large Language Models for intelligent reasoning."""
    
    def __init__(self, 
                 model_name: str = "microsoft/DialoGPT-medium",
                 use_pipeline: bool = True,
                 max_length: int = 512,
                 temperature: float = 0.7):
        """
        Initialize the LLM processor.
        
        Args:
            model_name: HuggingFace model name
            use_pipeline: Whether to use HuggingFace pipeline (easier) or direct model
            max_length: Maximum tokens in generated response
            temperature: Sampling temperature for generation
        """
        self.model_name = model_name
        self.use_pipeline = use_pipeline
        self.max_length = max_length
        self.temperature = temperature
        
        # Check if GPU is available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize model based on configuration
        self.model = None
        self.tokenizer = None
        self.generator = None
        
        try:
            self._initialize_model()
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            logger.info("Falling back to rule-based processing")
            self.model = None
    
    def _initialize_model(self):
        """Initialize the LLM model and tokenizer."""
        if self.use_pipeline:
            # Use HuggingFace pipeline for easier inference
            try:
                # Try with a lightweight conversational model first
                logger.info(f"Loading model pipeline: {self.model_name}")
                self.generator = pipeline(
                    "text-generation",
                    model=self.model_name,
                    tokenizer=self.model_name,
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    return_full_text=False,
                    max_new_tokens=256,
                    do_sample=True,
                    temperature=self.temperature,
                    pad_token_id=50256  # GPT-2 pad token
                )
                logger.info("Model pipeline loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load {self.model_name}: {e}")
                # Fallback to a smaller model
                fallback_model = "gpt2"
                logger.info(f"Trying fallback model: {fallback_model}")
                self.generator = pipeline(
                    "text-generation",
                    model=fallback_model,
                    device=0 if self.device == "cuda" else -1,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    return_full_text=False,
                    max_new_tokens=256,
                    do_sample=True,
                    temperature=self.temperature,
                    pad_token_id=50256
                )
                logger.info("Fallback model loaded successfully")
        else:
            # Direct model loading (more control but more complex)
            logger.info(f"Loading model and tokenizer: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info("Model and tokenizer loaded successfully")
    
    def is_available(self) -> bool:
        """Check if LLM is available for processing."""
        return (self.generator is not None) or (self.model is not None and self.tokenizer is not None)
    
    def generate_response(self, prompt: str, max_length: Optional[int] = None) -> str:
        """
        Generate a response using the LLM.
        
        Args:
            prompt: Input prompt for the LLM
            max_length: Override default max length
            
        Returns:
            Generated response text
        """
        if not self.is_available():
            raise Exception("LLM not available")
        
        try:
            if self.use_pipeline and self.generator:
                # Use pipeline for generation
                outputs = self.generator(
                    prompt,
                    max_new_tokens=max_length or 256,
                    do_sample=True,
                    temperature=self.temperature,
                    pad_token_id=self.generator.tokenizer.pad_token_id
                )
                
                if outputs and len(outputs) > 0:
                    return outputs[0]['generated_text'].strip()
                else:
                    return "No response generated"
            
            else:
                # Direct model inference
                inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        inputs,
                        max_length=inputs.shape[1] + (max_length or 256),
                        do_sample=True,
                        temperature=self.temperature,
                        pad_token_id=self.tokenizer.pad_token_id,
                        attention_mask=torch.ones_like(inputs)
                    )
                
                # Decode only the generated part
                generated = outputs[0][inputs.shape[1]:]
                response = self.tokenizer.decode(generated, skip_special_tokens=True)
                return response.strip()
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def analyze_insurance_query(self, query: str, context: str, sources: List[Dict]) -> Dict:
        """
        Analyze an insurance query using LLM reasoning.
        
        Args:
            query: User query
            context: Relevant document context
            sources: Source information
            
        Returns:
            Analysis result with decision, amount, and justification
        """
        if not self.is_available():
            logger.warning("LLM not available, falling back to rule-based analysis")
            return self._fallback_analysis(query, context, sources)
        
        try:
            # Create a structured prompt for insurance analysis
            prompt = self._create_insurance_prompt(query, context, sources)
            
            # Generate LLM response
            response = self.generate_response(prompt, max_length=300)
            
            # Parse the LLM response
            parsed_result = self._parse_insurance_response(response, sources)
            
            return parsed_result
            
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            logger.info("Falling back to rule-based analysis")
            return self._fallback_analysis(query, context, sources)
    
    def _create_insurance_prompt(self, query: str, context: str, sources: List[Dict]) -> str:
        """Create a structured prompt for insurance claim analysis."""
        
        prompt = f"""
You are an insurance claim analyst. Analyze the following claim query against the policy documents.

QUERY: {query}

RELEVANT POLICY CONTEXT:
{context}

TASK: Analyze if this claim should be approved or rejected based on the policy terms.

Please provide your analysis in the following format:
DECISION: [Approved/Rejected/Under Review]
AMOUNT: [Specific amount if covered, or "N/A"]
JUSTIFICATION: [Brief explanation referencing specific policy clauses]

Analysis:"""
        
        return prompt
    
    def _parse_insurance_response(self, response: str, sources: List[Dict]) -> Dict:
        """Parse LLM response into structured format."""
        
        # Initialize default values
        decision = "Under Review"
        amount = "TBD"
        justification = "Analysis in progress"
        
        try:
            # Simple parsing of the LLM response
            lines = response.split('\n')
            
            for line in lines:
                line = line.strip()
                if line.startswith('DECISION:'):
                    decision = line.replace('DECISION:', '').strip()
                elif line.startswith('AMOUNT:'):
                    amount = line.replace('AMOUNT:', '').strip()
                elif line.startswith('JUSTIFICATION:'):
                    justification = line.replace('JUSTIFICATION:', '').strip()
                elif 'approved' in line.lower() and decision == "Under Review":
                    decision = "Approved"
                elif 'rejected' in line.lower() and decision == "Under Review":
                    decision = "Rejected"
            
            # Add source information to justification
            source_names = [s.get('source', 'unknown') for s in sources[:3]]
            justification += f" (Sources: {', '.join(set(source_names))})"
            
        except Exception as e:
            logger.warning(f"Failed to parse LLM response: {e}")
            justification = f"LLM generated: {response[:200]}..."
        
        return {
            "decision": decision,
            "amount": amount,
            "justification": justification,
            "llm_response": response,
            "analysis_method": "LLM-based"
        }
    
    def _fallback_analysis(self, query: str, context: str, sources: List[Dict]) -> Dict:
        """Fallback rule-based analysis when LLM is not available."""
        
        query_lower = query.lower()
        context_lower = context.lower()
        
        # Simple pattern matching
        decision = "Under Review"
        amount = "To be determined"
        justification = f"Rule-based analysis of {len(sources)} document sections. "
        
        # Check for coverage indicators
        if any(word in context_lower for word in ["covered", "eligible", "approved"]):
            decision = "Likely Approved"
            justification += "Context indicates coverage eligibility. "
            
            # Look for amount patterns
            import re
            amount_patterns = re.findall(r'₹[\d,]+|rs\.?\s*[\d,]+', context_lower)
            if amount_patterns:
                amount = amount_patterns[0]
                justification += f"Amount reference found: {amount}. "
        
        elif any(word in context_lower for word in ["not covered", "excluded", "rejected"]):
            decision = "Likely Rejected"
            justification += "Context indicates potential exclusion. "
        
        # Add source information
        source_names = [s.get('source', 'unknown') for s in sources[:3]]
        justification += f"(Sources: {', '.join(set(source_names))})"
        
        return {
            "decision": decision,
            "amount": amount,
            "justification": justification,
            "llm_response": "Rule-based analysis used",
            "analysis_method": "Rule-based fallback"
        }
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model."""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "available": self.is_available(),
            "use_pipeline": self.use_pipeline,
            "max_length": self.max_length,
            "temperature": self.temperature
        }

# Convenience functions
def create_llm_processor(**kwargs) -> LLMProcessor:
    """Create an LLM processor with default settings."""
    return LLMProcessor(**kwargs)

def get_recommended_model() -> str:
    """Get recommended model based on available resources."""
    if torch.cuda.is_available():
        # If GPU available, can use larger models
        return "microsoft/DialoGPT-medium"
    else:
        # For CPU, use smaller model
        return "gpt2"