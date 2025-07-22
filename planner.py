import requests
import json
import os

PROMPT_TEMPLATE = """
I am spending a weekend in {city}. My mood is {mood} and I’m interested in {interests_str}. I have {total_hours} hours free over Saturday and Sunday.

Suggest a realistic, fun, and well-paced 2-day weekend itinerary.
Include specific activity names, brief descriptions, suggested timings for each activity, and incorporate suitable breaks and food spots.
Please ensure the total time spent on activities and breaks on both days combined does not exceed {total_hours} hours.
Prioritize real places if possible and use relevant emojis.

Format the output using Markdown with clear headings for each day and bullet points for activities. For example:

### Your Weekend Plan in [City Name] 🎉

**Saturday**
- ⏰ [Start Time] – [End Time]: [Activity Name] [Emoji] - [Brief description]. (e.g., Duration: X hours)
- 🍕 [Time]: Lunch break.

**Sunday**
- ⏰ [Start Time] – [End Time]: [Activity Name] [Emoji] - [Brief description]. (e.g., Duration: Y hours)
- ☕ [Time]: Coffee break.
"""

def generate_llm_plan(city, mood, interests, total_hours):
    interests_str = ", ".join(interests) if interests else "anything interesting"

    prompt = PROMPT_TEMPLATE.format(
        city=city,
        mood=mood,
        interests_str=interests_str,
        total_hours=total_hours
    )

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        return "Error: OpenRouter API key not found. Please set the OPENROUTER_API_KEY environment variable/secret."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    model_name = "mistralai/mistral-7b-instruct"
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data and 'choices' in data and data['choices']:
            return data['choices'][0]['message']['content']
        else:
            return f"Error: Unexpected response format from LLM. Raw data: {data}. Please try again."

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return f"Error: Failed to get a plan from the AI. API Request issue: {e}. Please check your API key and internet connection."
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        print(f"Raw response: {response.text if 'response' in locals() else 'No response received'}")
        return "Error: Could not parse AI response. Please try again or check logs for details."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"