import asyncio
from aiobotocore.session import get_session

import s3_fetchers

import near_types
from typing import Union


AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"

config = near_types.LakeConfig(
    "near-lake-data-mainnet",
    "eu-central-1",
    69130938,
    10
)


async def start():  # config: near_types.LakeConfig
    session = get_session()
    async with session.create_client(
        "s3", region_name=config.s3_region_name,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_access_key_id=AWS_ACCESS_KEY_ID
    ) as s3_client:
        start_from_block_height = config.start_block_height
        last_processed_block_hash: Union[near_types.CryptoHash, None] = None

        while True:
            block_heights_prefixes = await s3_fetchers.list_blocks(
                s3_client,
                config.s3_bucket_name,
                start_from_block_height,
                config.blocks_preload_pool_size * 2
            )

            if len(block_heights_prefixes) == 0:
                print("No new blocks on S3, retry in 2s...")

                await asyncio.sleep(2)
                continue

            print(
                "Received {} blocks from S3"
                .format(len(block_heights_prefixes))
            )

            streamer_messages_queue = asyncio.Queue(
                maxsize=config.blocks_preload_pool_size
            )
            pending_block_heights = iter(block_heights_prefixes)

            for _ in range(streamer_messages_queue.qsize()):
                block_height = next(pending_block_heights)
                streamer_messages_queue.put(
                    s3_fetchers.fetch_streamer_message(
                        s3_client,
                        config.s3_bucket_name,
                        block_height
                    )
                )

            while not streamer_messages_queue.empty():
                streamer_message = await streamer_messages_queue.get()

                if last_processed_block_hash != streamer_message.block.prev_hash:
                    print(
                        "`prev_hash` does not match, refetching the data from S3 in 200ms"
                    )

                    await asyncio.sleep(0.2)
                    break

                last_processed_block_hash = streamer_message.block.header.hash
                start_from_block_height = streamer_message.block.header.height + 1

                pending_block_height = pending_block_heights.next()
                streamer_messages_queue.put(
                    s3_fetchers.fetch_streamer_message(
                        s3_client,
                        config.s3_bucket_name,
                        pending_block_height,
                    )
                )


loop = asyncio.get_event_loop()
cors = asyncio.wait([start()])
loop.run_until_complete(cors)
