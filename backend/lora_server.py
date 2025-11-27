from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
import io
import torch
from diffusers import StableDiffusionPipeline
from peft import PeftModel

BASE_MODEL = "runwayml/stable-diffusion-v1-5" 
LORA_PATH = "./lora_output" 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading base model...")
pipe = StableDiffusionPipeline.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)

print("Loading LoRA weights...")
pipe.unet.load_attn_procs(LORA_PATH)

if torch.cuda.is_available():
    pipe.to("cuda")
else:
    pipe.to("cpu")

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate(prompt: Prompt):
    image = pipe(prompt.prompt).images[0]

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    img_bytes = base64.b64encode(buffer.getvalue()).decode()

    return JSONResponse({"image": img_bytes})
