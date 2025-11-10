import pandas as pd


def save_coins(username: str, coins: int, dir_path: str) -> None:
    """Save coins for a user."""
    # This is a placeholder implementation.
    df = pd.DataFrame({"username": [username], "coins": [coins]})
    df.to_csv(f"{dir_path}/{username}_coins.csv", index=False)
