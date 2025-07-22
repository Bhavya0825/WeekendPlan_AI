from planner import generate_llm_plan
from dotenv import load_dotenv
load_dotenv()
import gradio as gr
import os

def create_downloadable_plan(plan_text, city):
    safe_city_name = "".join(c for c in city if c.isalnum() or c in (' ', '.', '_')).replace(' ', '_')
    filename = f"weekend_plan_{safe_city_name}.md"
    
    os.makedirs("temp", exist_ok=True)
    filepath = os.path.join("temp", filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(plan_text)
    return filepath

def get_plan_and_download_file(city, mood, interests, total_hours):
    if not city.strip():
        return "Please enter a city name to get a plan.", None

    llm_output = generate_llm_plan(city, mood, interests, total_hours)
    
    download_filepath = None
    if not llm_output.startswith("Error:"):
        download_filepath = create_downloadable_plan(llm_output, city)
    
    return llm_output, download_filepath

with gr.Blocks(theme=gr.themes.Soft(), title="WeekendPlan AI") as demo:
    gr.Markdown(
        """
        # 🧭 WeekendPlan AI 🌆🗓️🎯
        ### *Your AI for perfect weekend escapes.* """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## Your Weekend Preferences")
            
            city_input = gr.Textbox(
                label="Where are you planning to go?",
                placeholder="e.g., Hyderabad, London, Kyoto...",
                interactive=True,
                value="Hyderabad"
            )
            mood_input = gr.Dropdown(
                choices=["Relaxed 🧘‍♀️", "Adventurous ⛰️", "Cultural 🏛️", "Romantic ❤️", "Family Fun 👨‍👩‍👧‍👦", "Party 🎉", "Solo Exploration 🚶‍♂️"],
                label="What's your weekend mood?",
                value="Relaxed 🧘‍♀️",
                interactive=True
            )
            interests_input = gr.CheckboxGroup(
                choices=["Art 🎨", "Food 🍜", "Nature 🌳", "Shopping 🛍️", "Music 🎶", "History 📜", "Nightlife 🕺", "Wellness ✨", "Photography 📸", "Sports ⚽"],
                label="What are you interested in? (Select all that apply)",
                interactive=True
            )
            total_hours_input = gr.Slider(
                minimum=6, 
                maximum=20, 
                value=14,
                step=0.5, 
                label="Total Activity Hours (over Sat & Sun)",
                info="This includes time for activities, travel between spots, and breaks. Adjust based on your energy level!"
            )

            with gr.Row():
                generate_button = gr.Button("✨ Generate My Weekend Plan ✨", variant="primary", scale=2)
                clear_button = gr.Button("Clear All Inputs", scale=1)

        with gr.Column(scale=2):
            gr.Markdown("## Your Custom-Crafted Itinerary")
            output_plan = gr.Markdown(label="Your Personalized Weekend Plan")
            download_file_output = gr.File(label="Download Your Plan (.md)", file_count="single", interactive=False) 

    generate_button.click(
        fn=get_plan_and_download_file,
        inputs=[city_input, mood_input, interests_input, total_hours_input],
        outputs=[output_plan, download_file_output],
        show_progress=True
    )
    
    clear_button.click(
        fn=lambda: (None, "Relaxed 🧘‍♀️", [], 14, "", None),
        inputs=[],
        outputs=[city_input, mood_input, interests_input, total_hours_input, output_plan, download_file_output]
    )

demo.launch(share=True, debug=True)