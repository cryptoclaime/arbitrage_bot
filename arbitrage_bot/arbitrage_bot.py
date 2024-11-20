import os
from dotenv import load_dotenv
from binance.client import Client
import itertools

# Load environment variables from .env file
load_dotenv()

# Fetch API Key and Secret from environment variables
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Trade amount (you can change this value for manual testing)
TRADE_AMOUNT = 30.0  # USDT
MIN_PROFIT_THRESHOLD = 0.3  # Minimum profit to stop the bot (in USDT)
MIN_PROFIT_PERCENTAGE = 0.5  # Minimum profit percentage to stop the bot

def fetch_price(symbol):
    """Fetch the current price of a symbol from Binance."""
    try:
        price = client.get_symbol_ticker(symbol=symbol)["price"]
        return float(price)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def load_all_valid_pairs():
    """Fetch all valid trading pairs from Binance."""
    try:
        exchange_info = client.get_exchange_info()
        valid_pairs = [symbol["symbol"] for symbol in exchange_info["symbols"] if symbol["status"] == "TRADING"]
        return valid_pairs
    except Exception as e:
        print(f"Error fetching exchange info: {e}")
        return []

def calculate_profit(initial_amount, price1, price2, price3, pair1, pair2, pair3):
    """Calculate profit percentage for triangular arbitrage."""
    try:
        # A -> B (pair1)
        amount_in_b = initial_amount / price1
        # B -> C (pair2)
        amount_in_c = amount_in_b * price2
        # C -> A (pair3)
        final_amount = amount_in_c * price3

        # Calculate profit percentage
        profit = final_amount - initial_amount
        profit_percentage = (profit / initial_amount) * 100 if final_amount > initial_amount else 0

        return final_amount, profit, profit_percentage, pair1, pair2, pair3
    except Exception as e:
        print(f"Error calculating profit: {e}")
        return initial_amount, 0, 0, None, None, None  # Return no profit

def find_triangular_arbitrage(pairs, initial_amount):
    """Look for triangular arbitrage opportunities among the trading pairs."""
    for pair1, pair2, pair3 in itertools.combinations(pairs, 3):
        # Extract the base and quote assets from each pair
        base1, quote1 = pair1[:3], pair1[3:]
        base2, quote2 = pair2[:3], pair2[3:]
        base3, quote3 = pair3[:3], pair3[3:]
        
        # Check if we can form a cycle A -> B -> C -> A
        if base1 == base2 and quote2 == base3 and quote3 == quote1:
            # If valid, check prices
            price1 = fetch_price(pair1)
            price2 = fetch_price(pair2)
            price3 = fetch_price(pair3)
            
            if price1 and price2 and price3:
                # Calculate potential arbitrage cycle: A -> B -> C -> A
                final_amount, profit, profit_percentage, pair1, pair2, pair3 = calculate_profit(
                    initial_amount, price1, price2, price3, pair1, pair2, pair3
                )
                
                # Print the token pairs, profit, and percentage while running
                if profit > 0:
                    print(f"Arbitrage Opportunity Found!")
                    print(f"Token Pairs: {pair1} -> {pair2} -> {pair3}")
                    print(f"Buy {base1}/{quote1} -> Sell {base2}/{quote2} -> Buy {base2}/{quote2} -> Sell {base3}/{quote3} -> Buy {base3}/{quote3} -> Sell {base1}/{quote1}")
                    print(f"Initial Amount: {initial_amount} USDT")
                    print(f"Final Amount: {final_amount:.2f} USDT")
                    print(f"Profit: {profit:.4f} USDT ({profit_percentage:.2f}%)")

                # If profit is greater than or equal to the minimum threshold, stop the bot
                if profit >= MIN_PROFIT_THRESHOLD:
                    print(f"Minimum profit of {MIN_PROFIT_THRESHOLD} USDT reached. Stopping the bot.")
                    return True  # Stop the bot

    return False

def main():
    print("Starting arbitrage scanner...")

    # Fetch all valid trading pairs available on Binance
    valid_pairs = load_all_valid_pairs()

    if not valid_pairs:
        print("No valid trading pairs found.")
        return

    # Look for triangular arbitrage opportunities
    found_opportunity = find_triangular_arbitrage(valid_pairs, TRADE_AMOUNT)

    if not found_opportunity:
        print("No arbitrage opportunities found.")

if __name__ == "__main__":
    main()
