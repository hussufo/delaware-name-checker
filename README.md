# Delaware Corporate Name Checker

An automated tool to check corporate name availability in Delaware using Steel browser automation and OpenAI for result analysis.

## Features

- 🔍 **Automated Search**: Automatically searches the Delaware Division of Corporations database
- 🤖 **CAPTCHA Solving**: Uses Steel's API to solve CAPTCHAs automatically
- 🧠 **AI Analysis**: Leverages OpenAI to analyze search results and determine availability
- 📊 **Structured Output**: Returns availability status, cost information, and detailed messages

## Requirements

- Python 3.11+
- [Steel API](https://steel.dev) account and API key
- [OpenAI API](https://openai.com) account and API key

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd delaware-name-checker
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -e .
```

### 4. Set up environment variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:

```
STEEL_API_KEY=your_steel_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

```bash
python main.py
```

## Configuration

The script currently searches for "GEMINI AUTOMATION SERVICES" as a corporation. To change the search parameters, edit the following variables in `main.py`:

- `entity_name_to_check`: The business name to search for
- `entity_type`: Currently set to "C" (Corporation)
- `entity_ending`: Currently set to "CORPORATION"

## Output

The script will output:

- ✅ **Available**: If the name is available for registration, including estimated cost
- ❌ **Unavailable**: If the name is already taken or unavailable
- **AI Analysis**: Detailed message from OpenAI's analysis of the search results

## Error Handling

- Screenshots are automatically saved on errors for debugging
- HTML results are saved to `result_page_for_manual_review.html` if AI analysis fails
- Detailed error messages are provided for API failures

## API Keys Setup

### Steel API

1. Sign up at [steel.dev](https://steel.dev)
2. Get your API key from the dashboard
3. Add it to your `.env` file as `STEEL_API_KEY`

### OpenAI API

1. Sign up at [openai.com](https://openai.com)
2. Create an API key in your account dashboard
3. Add it to your `.env` file as `OPENAI_API_KEY`

## Troubleshooting

- **CAPTCHA Issues**: If CAPTCHA solving fails, check your Steel API key and ensure your account has sufficient credits
- **OpenAI Errors**: Verify your OpenAI API key is valid and has sufficient credits
- **Browser Connection**: If browser connection fails, check your internet connection and Steel API status

## License

This project is for educational and research purposes only. Please comply with the Delaware Division of Corporations' terms of service when using this tool.
