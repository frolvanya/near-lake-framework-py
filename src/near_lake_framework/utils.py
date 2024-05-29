import json

import requests

from near_lake_framework import Network, near_primitives


def fetch_latest_block(
    network: Network = Network.MAINNET, timeout: int = 10
) -> near_primitives.BlockHeight:
    """
    Define the RPC endpoint for the NEAR network
    """
    url = f"https://rpc.{network}.near.org"

    # Define the payload for fetching the latest block
    payload = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": "dontcare",
            "method": "block",
            "params": {"finality": "final"},
        }
    )

    # Define the headers for the HTTP request
    headers = {"Content-Type": "application/json"}

    # Send the HTTP request to the NEAR RPC endpoint
    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=timeout
    )

    # Parse the JSON response to get the latest final block height
    latest_final_block: int = response.json()["result"]["header"]["height"]

    return latest_final_block
