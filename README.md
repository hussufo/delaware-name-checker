# Delaware Corporate Name Checker

An automated tool to check corporate name availability in Delaware using Steel browser automation and OpenAI for result analysis.

## Requirements

- Python 3.11+
- [Steel API](https://steel.dev) account and API key
- [OpenAI API](https://openai.com) account and API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/hussufo/delaware-name-checker
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
pip install -r requirements.txt
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

### Basic Usage

```bash
python main.py "YOUR COMPANY NAME"
```

### With Entity Type Selection

```bash
python main.py "YOUR COMPANY NAME" --entity-type corporation
```

### Available Entity Types

- `corporation` (default)
- `statutory_trust`
- `limited_partnership`
- `limited_liability_partnership`
- `limited_liability_company`
- `general_partnership`
- `llc_registered_series`
- `lp_registered_series`

### Examples

```bash
# Check a corporation name (default)
python main.py "GEMINI AUTOMATION SERVICES"

# Check an LLC name
python main.py "TECH SOLUTIONS LLC" --entity-type limited_liability_company

# Check a limited partnership
python main.py "INVESTMENT PARTNERS LP" --entity-type limited_partnership

# Check a statutory trust
python main.py "PROPERTY TRUST" --entity-type statutory_trust
```

### Help

```bash
python main.py --help
```

## Configuration

The script now accepts command-line arguments for:

- **Entity Name**: The business name to search for (required argument)
- **Entity Type**: The type of entity to check (optional, defaults to "corporation")

No manual code editing is required - all configuration is done through command-line arguments.

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
