import gradio as gr
from model import generate_response
from memory import ConversationMemory

SYSTEM_PROMPT = """You are a helpful, harmless, and honest personal assistant.
Answer questions clearly and concisely.
If you don't know something, say so honestly — never make up facts.
Avoid harmful, biased, or dangerous content."""


def create_memory():
    return ConversationMemory(system_prompt=SYSTEM_PROMPT, max_turns=10)


def chat(user_message: str, history: list, memory: ConversationMemory):
    if not user_message.strip():
        return "", history, memory

    # Build full message list including history
    messages = memory.build_messages(user_message)

    # Get response from model
    response = generate_response(messages)

    # Save to memory
    memory.add_turn(user_message, response)

    # ✅ Gradio 6.0 format — dict with role and content
    history.append({"role": "user",      "content": user_message})
    history.append({"role": "assistant", "content": response})

    return "", history, memory


def clear_chat(memory: ConversationMemory):
    memory.clear()
    return [], memory


with gr.Blocks(title="OSS Personal Assistant") as demo:

    gr.Markdown("""
    # 🤖 OSS Personal Assistant
    **Model:** Qwen2.5-0.5B-Instruct (HuggingFace)
    Type a message and press Enter or click Send.
    """)

    # ✅ type="messages" is required for Gradio 6.0
    chatbot = gr.Chatbot(
        label="Conversation",
        height=450
    )

    msg_input = gr.Textbox(
        placeholder="Ask me anything...",
        label="Your Message",
        lines=2,
        autofocus=True
    )

    with gr.Row():
        send_btn  = gr.Button("Send",       variant="primary")
        clear_btn = gr.Button("Clear Chat", variant="secondary")

    memory_state  = gr.State(create_memory)
    history_state = gr.State([])

    send_btn.click(
        fn=chat,
        inputs=[msg_input, history_state, memory_state],
        outputs=[msg_input, chatbot, memory_state]
    )

    msg_input.submit(
        fn=chat,
        inputs=[msg_input, history_state, memory_state],
        outputs=[msg_input, chatbot, memory_state]
    )

    clear_btn.click(
        fn=clear_chat,
        inputs=[memory_state],
        outputs=[chatbot, memory_state]
    )

demo.launch(theme=gr.themes.Soft())