import os
import openai
from typing import Optional

# Get API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY = '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'
if not OPENAI_API_KEY: raise ValueError("Please set the OPENAI_API_KEY environment variable")
openai.api_key = OPENAI_API_KEY

def generate_poem(prompt: str) -> Optional[str]:
    """
    Generate a poem using OpenAI's API based on a prompt about someone.
    
    Args:
        prompt (str): A description of the person or situation to write a poem about
        
    Returns:
        str: The generated poem, or None if generation failed
    """
    try:
        # Create the system prompt to guide the poem generation
        system_prompt = """You are a skilled poet. Create a short, meaningful poem about the person or situation described.
        The poem should be:
        - 4-6 lines long
        - Easy to understand
        - Emotionally resonant
        - Suitable for text-to-speech
        """
        
        # Make the API call
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Write a poem about: {prompt}"}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        # Extract the poem from the response
        poem = response.choices[0].message.content.strip()
        return poem
        
    except Exception as e:
        print(f"Error generating poem: {str(e)}")
        return None

def main():
    # Example prompt - you can modify this
    prompt = "her name is sarah, she's famous."

    poem = generate_poem(prompt)
    if poem:
        print(poem)
        
        # Save the poem to a file
        with open("poem.txt", "w") as f:
            f.write(poem)
        print("\nPoem has been saved to poem.txt")

if __name__ == "__main__":
    main()
