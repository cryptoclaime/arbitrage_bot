from dotenv import load_dotenv
from binance.client import Client
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch API Key and Secret from environment variables
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Debug: Print API Key and Secret to confirm they're loaded (remove in production)
if not api_key or not api_secret:
    print("Error: API key or secret not found. Check your .env file.")
else:
    print(f"API Key: {api_key}")
    print(f"API Secret: {api_secret}")

# Initialize Binance client with API keys
client = Client(api_key, api_secret)

# Test API connection
try:
    account_info = client.get_account()  # Fetch account details
    print("Successfully connected to Binance!")
    print("Account Information:")
    print(account_info)
except Exception as e:
    print(f"Error connecting to Binance API: {e}")
