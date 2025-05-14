from google import genai
import os


def get_search_query(num_queries=30, category=None):

    prompt = f"Generate {num_queries} interesting and diverse search queries"
    if category:
        prompt += f" related to {category}"
    prompt += ". Respond with ONLY the search queries, one per line, without numbering or any other text."
    print(prompt)
    return prompt


def execute_prompt(prompt):
    model = os.environ.get("GEMINI_MODEL")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(model=model, contents=prompt)
        
        # Split the response into individual queries
        queries = response.text.strip().split("\n")
        # Clean up any empty queries
        queries = [q for q in queries if q.strip()]
        
        print(f"Queries: {queries}")
        return queries
    
    except Exception as e:
        print(f"Error generating queries: {e}")
        return
