# -*- coding: utf-8 -*-
"""

Generated from Colab notebook and edited as needed - initally ran using GPUs and had to make edits.

"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import os

# Setup because of issues running on personal computer 
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"  
os.environ["TQDM_DISABLE"] = "1"                    
os.environ["TOKENIZERS_PARALLELISM"] = "false"      

ADAPTER_DIR = "os.getenv("ADAPTER_DIR", "/CHANGE/THIS/PATH")" # Folder for where LoRA adapter/tokenizer lives
BASE_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"  # HuggingFace model for base
PROMPT = "You are a careful, empathetic, clinical assistant. You will first ask about medical history, then, symptoms. Once you have this information, you will make a determination of what condition you think they have, and any tests or imaging you will need to run. You may not need to run tests or imaging. You will share this information with your patient, creating a considerate treatment plan, and being sure to address any questions or concerns they may have."

# Super-simple chat session
class Chat:
    def __init__(self, model, tokenizer, system="You are a careful, empathetic clinical assistant."):
        self.model = model
        self.tok = tokenizer
        self.messages = [{"role": "system", "content": system}]
        # Speed/Stability
        torch.backends.cuda.matmul.allow_tf32 = True
        self.model.config.use_cache = True  

    # Generate the response from the model, basically where the money is!
    def say(self, user_text, max_new_tokens=256, sample=True, temperature=0.7):
        self.messages.append({"role": "user", "content": user_text})
        prompt = self.tok.apply_chat_template(self.messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tok([prompt], return_tensors="pt").to(next(self.model.parameters()).device)

        eos_ids = [self.tok.eos_token_id]
        im_end_id = self.tok.convert_tokens_to_ids("<|im_end|>")
        if im_end_id is not None and im_end_id != self.tok.unk_token_id:
          eos_ids.append(im_end_id)


        gen_kwargs = dict(
            max_new_tokens=max_new_tokens,
            eos_token_id=eos_ids,
            pad_token_id=self.tok.eos_token_id,
            repetition_penalty=1.15,
        )
        if sample:
            gen_kwargs.update(dict(do_sample=True, temperature=temperature))
        else:
            gen_kwargs.update(dict(do_sample=False))

        with torch.no_grad():
            out = self.model.generate(**inputs, **gen_kwargs)

        new_tokens = out[0, inputs["input_ids"].shape[-1]:]
        reply = self.tok.decode(new_tokens, skip_special_tokens=True).strip()
        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def reset(self, system=None):
        system = system or self.messages[0]["content"]
        self.messages = [{"role": "system", "content": system}]

def load_model_and_tokenizer(model_name : str, adapter_dir : str):
  tokenizer = AutoTokenizer.from_pretrained(adapter_dir, use_fast=True)
  # base model, then lora
  model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="float32", device_map="cpu")
  model = PeftModel.from_pretrained(model, adapter_dir)

  if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
  model.eval()
  torch.backends.cuda.matmul.allow_tf32 = True

  return tokenizer, model

def main():
  print("Loading model...")
  tokenizer, model = load_model_and_tokenizer(BASE_MODEL, ADAPTER_DIR)
  chat = Chat(model, tokenizer, system=PROMPT)
  print("Model loaded. Starting chat...")

  while True:
    user = input("You: ").strip()
    if user.lower() in {"quit","exit",""}:
        break
    print("Assistant:", chat.say(user))

if __name__ == "__main__":
    main()
