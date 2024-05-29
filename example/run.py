import asyncio
import logging
import os

from near_lake_framework import LakeConfig, streamer, Network
from near_lake_framework.utils import fetch_latest_block

# Suppress warning logs from specific dependencies
logging.getLogger("near_lake_framework").setLevel(logging.INFO)


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
