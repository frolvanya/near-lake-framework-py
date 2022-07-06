import asyncio
import itertools
import os
from typing import Optional

from aiobotocore.session import get_session

import near_primitives
import s3_fetchers

from dataclasses import dataclass

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')


@dataclass
class LakeConfig:
    s3_bucket_name: str
    s3_region_name: str
    start_block_height: near_primitives.BlockHeight
    blocks_preload_pool_size: int

    def mainnet(self) -> 'LakeConfig':
        self.s3_bucket_name = "near-lake-data-mainnet"
        self.s3_region_name = "eu-central-1"

        return self

    def testnet(self) -> 'LakeConfig':
        self.s3_bucket_name = "near-lake-data-testnet"
        self.s3_region_name = "eu-central-1"

        return self


async def start(config: LakeConfig, streamer_messages_queue: asyncio.Queue):
    session = get_session()
    async with session.create_client(
        "s3", region_name=config.s3_region_name,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_access_key_id=AWS_ACCESS_KEY_ID
    ) as s3_client:
        start_from_block_height: near_primitives.BlockHeight = config.start_block_height
        last_processed_block_hash: Optional[near_primitives.CryptoHash] = None

        while True:
            block_heights_prefixes = await s3_fetchers.list_blocks(
                s3_client,
                config.s3_bucket_name,
                start_from_block_height,
                config.blocks_preload_pool_size * 2
            )

            if not block_heights_prefixes:
                print("No new blocks on S3, retry in 2s...")

                await asyncio.sleep(2)
                continue

            print(
                "Received {} blocks from S3"
                .format(len(block_heights_prefixes))
            )

            pending_block_heights = iter(block_heights_prefixes)
            streamer_messages_futures = []
            for block_height in itertools.islice(pending_block_heights, streamer_messages_queue.maxsize):
                streamer_messages_futures.append(
                    asyncio.create_task(s3_fetchers.fetch_streamer_message(
                        s3_client,
                        config.s3_bucket_name,
                        block_height
                    ))
                )

            while streamer_messages_futures:
                streamer_message = await streamer_messages_futures.pop(0)

                if last_processed_block_hash and last_processed_block_hash != streamer_message.block.header.prev_hash:
                    print(
                        "`prev_hash` does not match, refetching the data from S3 in 200ms",
                        last_processed_block_hash,
                        streamer_message.block.header.prev_hash
                    )

                    await asyncio.sleep(0.2)
                    break

                last_processed_block_hash = streamer_message.block.header.hash
                start_from_block_height = streamer_message.block.header.height + 1

                try:
                    pending_block_height = next(pending_block_heights)
                except StopIteration:
                    pass
                else:
                    streamer_messages_futures.append(
                        asyncio.create_task(s3_fetchers.fetch_streamer_message(
                            s3_client,
                            config.s3_bucket_name,
                            pending_block_height,
                        ))
                    )

                await streamer_messages_queue.put(streamer_message)


def streamer(config: LakeConfig):
    streamer_messages_queue: asyncio.Queue = asyncio.Queue(
        maxsize=config.blocks_preload_pool_size
    )
    stream_handle = asyncio.create_task(start(config, streamer_messages_queue))
    return (stream_handle, streamer_messages_queue)

# import asyncio

# from near_lake_framework import near_types
# from near_lake_framework import streamer


# async def main():
#     config = near_types.LakeConfig(
#         s3_bucket_name="near-lake-data-mainnet",
#         s3_region_name="eu-central-1",
#         start_block_height=69130938,
#         blocks_preload_pool_size=10
#     )

#     stream_handle, streamer_messages_queue = streamer(config)
#     while True:
#         streamer_message = await streamer_messages_queue.get()
#         print(
#             f"Received Block #{streamer_message.block.header.height} from Lake Framework")
#         # await asyncio.sleep(1)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
