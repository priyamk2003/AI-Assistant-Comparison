import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# -----------------------------------------------------------
# MODEL CHOICE
# Using Qwen2.5-0.5B-Instruct because:
# - Very small (0.5B params), runs on CPU without issues
# - Supports chat format natively
# - Free to use, no HuggingFace token needed
# -----------------------------------------------------------
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# Use GPU if available, otherwise CPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE  = torch.float16 if DEVICE == "cuda" else torch.float32

print(f"Device : {DEVICE}")
print(f"Loading model — first run will download ~1GB, please wait...")

# Load tokenizer (converts text → numbers the model understands)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load the actual model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=DTYPE,
    device_map="auto" if DEVICE == "cuda" else None,
)

if DEVICE == "cpu":
    model = model.to(DEVICE)

model.eval()  # puts model in inference mode (no training)
print("Model loaded and ready.")


def generate_response(messages: list, max_new_tokens: int = 512) -> str:
    """
    Takes the full conversation as a list of messages.
    Returns the model's reply as a string.
    """

    # Convert messages into the exact text format this model expects
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    # Tokenize (text → numbers)
    inputs = tokenizer([text], return_tensors="pt").to(DEVICE)

    # Generate response
    with torch.no_grad():  # saves memory, we're not training
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,        # controls randomness (0=robotic, 1=creative)
            top_p=0.9,              # keeps only top 90% probable tokens
            repetition_penalty=1.1, # discourages repeating same phrases
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode ONLY the new tokens (not the input we sent)
    new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    response   = tokenizer.decode(new_tokens, skip_special_tokens=True)

    return response.strip()