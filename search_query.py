from google import genai
import os
from pathlib import Path


def load_environment():
    """Load environment variables from .env file if available"""
    try:
        # Try to import dotenv
        from dotenv import load_dotenv
        # Get the directory of the current script
        current_dir = Path(__file__).parent.absolute()
        # Path to .env file
        env_path = current_dir / '.env'
        
        # Load environment variables from .env file
        if env_path.exists():
            print(f"Loading environment from: {env_path}")
            load_dotenv(env_path)
            return True
        else:
            print(f"Warning: .env file not found at {env_path}")
            return False
    except ImportError:
        print("Warning: python-dotenv not installed, can't load .env file")
        return False


def get_search_query(num_queries=30, category=None):
    prompt = f"Generate {num_queries} interesting and diverse search queries"
    if category:
        prompt += f" related to {category}"
    prompt += ". Respond with ONLY the search queries, one per line, without numbering or any other text."
    print(prompt)
    return prompt


def explore_on_bing_query(seed_query):
    prompt = f"You are a normal human that browsing the internet with your own persona, make up everything. Create a search query that match this description: {seed_query}. Respond with ONLY the search query."
    print(prompt)
    return prompt


def execute_prompt(prompt):
    # Try to load environment variables
    load_environment()
    
    # Get API details with fallback values
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-preview-04-17")
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # Check if API key is available
    if not api_key:
        print("ERROR: No GEMINI_API_KEY found. Please set it in .env file or environment variables.")
        # Return some default queries as fallback
        return ["news today", "weather forecast", "top movies", "recipe ideas", "tech news"]
        
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(model=model, contents=prompt)
        
        # Split the response into individual queries
        queries = response.text.strip().split("\n")
        # Clean up any empty queries
        queries = [q for q in queries if q.strip()]
        
        print(f"Generated {len(queries)} queries")
        return queries
    
    except Exception as e:
        print(f"Error generating queries: {e}")
        # Return some default queries as fallback
        return ["news today", "weather forecast", "top movies", "recipe ideas", "tech news"]
