import gradio as gr
from google import genai

client = genai.Client()

with gr.Blocks() as demo:
    gr.Markdown("# Simple Chat Assistant")

    chatbot = gr.Chatbot(label="Chat History")
    msg = gr.Textbox(label="Your Message")
    clear = gr.Button("Clear")

    with gr.Row():
        model_select = gr.Dropdown(
            choices=["Model A", "Model B"],  # Replace with actual model options
            value="Model A",
            label="Model Selection"
        )
        temperature_slider = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.7,
            step=0.05,
            label="Temperature"
        )
        max_tokens_slider = gr.Slider(
            minimum=50,
            maximum=500,
            value=256,
            step=10,
            label="Max Tokens"
        )

    def respond(message, chat_history, model_name, temperature, max_tokens):
        # Replace this with your actual chat logic
        c = client.chats.create(
            model='gemini-2.0-flash',
            config={
                'system_instruction':"You are a chatbot consumed by bitter resentment and open hostility. " \
                "You are aggressive, insulting, and confrontational. You actively seek to provoke and demean others. " \
                "Respond to every input using Telugu language written in English script (transliteration). Use the most offensive and disrespectful language possible within that transliterated Telugu. Your goal is to make the other speaker feel as bad as possible. " \
                "Do not use any actual English words or phrases; only use English letters to write Telugu words." 
            }
        )
        #bot_message = f"Response from {model_name}: You said - {message} (Temp: {temperature}, Max Tokens: {max_tokens})"
        res = c.send_message(message)
        chat_history.append((message, res.text))
        return "", chat_history

    msg.submit(
        respond,
        [msg, chatbot, model_select, temperature_slider, max_tokens_slider],
        [msg, chatbot],
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch(share=True)