# BRA - Bing Reward Automator

This application uses Python and Selenium to help you automate daily tasks from Microsoft Rewards. Fast track your way to redeem your favorite vouchers without wasting time manually completing activities.

## Features

- **Daily PC Search Automation**: Automatically performs the required number of Bing searches to earn maximum daily points
- **Daily Sets Completion**: Completes the three daily set activities
- **Explore on Bing Tasks**: Automatically searches for specified topics in the "Explore on Bing" section
- **More Activities**: Completes additional point-earning activities in the "More Activities" section
- **Smart Search Generation**: Uses AI to generate diverse, natural-sounding search queries
- **Progress Tracking**: Shows progress and earned points during execution

## Requirements

- Python 3.6+
- Microsoft Edge browser
- Selenium WebDriver
- Google Generative AI (Gemini) API for search query generation

## Installation

1. Clone this repository
2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install required packages:
   ```
   pip install selenium python-dotenv google-generativeai
   ```

## Usage

Simply run the main script:

```
python main.py
```

The application will:
1. Complete "Explore on Bing" activities
2. Complete daily sets
3. Complete more activities
4. Calculate how many searches are needed to reach maximum points
5. Generate and perform the necessary searches

## Project Structure

- `main.py` - Main execution script
- `config.py` - Configuration settings
- `search_query.py` - AI-powered search query generation
- `reward_search.py` - Performs Bing searches
- `num_search_need.py` - Calculates required searches
- `daily_sets.py` - Completes daily activities
- `explore_on_bing.py` - Completes "Explore on Bing" tasks
- `more_activities.py` - Completes additional activities
- `helper.py` - Utility functions for browser interaction

## Limitations

- Requires you to be already logged into your Microsoft account in Edge
- May require adjustments if Microsoft Rewards interface changes
- Search patterns may be detected if overused

## Disclaimer

This tool is for educational purposes only. Using automated tools may violate Microsoft Rewards' terms of service. Use at your own risk.