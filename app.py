import gradio as gr
from llms import ChatGPT_response


description = '''
<h1 style="text-align: center; font-size: 40px;"><strong>Consti<span style='color: #964B00;'>Chat⚖️👨‍⚖️</span></strong></h1>
<br />
<span style='font-size: 18px;'>
Welcome to ConstiChat, an immersive space powered by ChatGPT and trained on the Constitution of South Africa. 
Engage in a playfully educational background where you can explore and delve into the depths of constitutional knowledge. 
Whether you're a legal scholar, a student, or simply curious about the South African constitution, ConstiChat is here to provide a captivating experience that enlightens and educates. 
Get ready to embark on an enlightening adventure as you navigate the nuances and intricacies of the Constitution of South Africa with the powerful assistance of ConstiChat.
</span>
'''

footnote = '''
**This product is provided strictly for educational and research purposes. 
The information provided by this model should not be considered as legal advice. 
It is strongly recommended to consult with a qualified legal professional for any legal matters or concerns. 
The content generated by this AI language model is purely speculative and may not be accurate, complete, or up-to-date. 
The creators of this model do not accept any liability for any actions taken based on the information provided. 
Users should exercise their own judgment and discretion when utilizing this product.**
'''

theme = gr.themes.Monochrome(
    primary_hue='indigo',
    secondary_hue='blue',
    neutral_hue='slate',
    radius_size=gr.themes.sizes.radius_sm,
    font=[gr.themes.GoogleFont('Open Sans'), 'ui-sans-serif', 'system-ui', 'sans-serif']
)

with gr.Blocks(title='ConstiChat⚖️👨‍', theme=theme) as demo:
    gr.Markdown(description, interactive=False)
    chatbot = gr.Chatbot(label='The Constitution of the Republic of South Africa, 1996', elem_id='chatbot_id')#.style(height=850)
    query = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    clear = gr.Button('Clear')
    
    def user(user_message, history):
        return gr.update(value="", interactive=False), history + [[user_message, None]]

    def bot_response(history):
        bot_message = '⚖️👨‍\n' + ChatGPT_response(history[-1][0]) 
        history[-1][1] = ""
        for character in bot_message:
            history[-1][1] += character
            yield history
    
    response = query.submit(user, [query, chatbot], [query, chatbot], queue=False).then(
        bot_response, chatbot, chatbot
    )
    response.then(lambda: gr.update(interactive=True), None, [query], queue=False)
    clear.click(lambda: None, None, chatbot, queue=False)    
    gr.Markdown(footnote)
demo.queue(concurrency_count=10)
demo.launch(height='800px', debug=True)