# Debugging permissions and connection
try:
    account_status = client.get_account_status()
    print(f"Account Status: {account_status}")
except Exception as e:
    print(f"Failed to retrieve account status: {e}")
