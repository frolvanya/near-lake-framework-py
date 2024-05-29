import asyncio
import json
import logging
import os

# This is not a direct dependency of NLF pip install requests to run
import requests

from near_lake_framework import LakeConfig, streamer, Network, near_primitives

REQUEST_TIMEOUT = 10
# Suppress warning logs from specific dependencies
logging.getLogger("near_lake_framework").setLevel(logging.INFO)


def fetch_latest_block(
    network: Network = Network.MAINNET,
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
        "POST", url, headers=headers, data=payload, timeout=REQUEST_TIMEOUT
    )

    # Parse the JSON response to get the latest final block height
    latest_final_block: int = response.json()["result"]["header"]["height"]

    return latest_final_block


async def main():
    network = Network.TESTNET
    latest_final_block = fetch_latest_block(network=network)
    config = LakeConfig(
        network,
        start_block_height=latest_final_block,
        # These fields must be set!
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    stream_handle, streamer_messages_queue = streamer(config)
    while True:
        streamer_message = await streamer_messages_queue.get()
        print(
            f"Received Block #{streamer_message.block.header.height} from Lake Framework"
        )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
