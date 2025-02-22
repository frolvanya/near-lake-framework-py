from __future__ import annotations
import asyncio
import itertools
from enum import Enum

import logging
from typing import Optional
from dataclasses import dataclass

from aiobotocore.session import get_session

from near_lake_framework import near_primitives
from near_lake_framework import s3_fetchers


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)


class Network(Enum):
    MAINNET = "mainnet"
    TESTNET = "testnet"

    @staticmethod
    def from_string(value: str):
        try:
            return Network(value.lower())
        except ValueError as err:
            valid_values = [v.value for v in Network]
            raise ValueError(
                f"Unknown network: {value}. Valid values are: {valid_values}"
            ) from err

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


@dataclass
class LakeConfig:
    s3_bucket_name: str
    s3_region_name: str
    aws_access_key_id: str
    aws_secret_key: str
    start_block_height: near_primitives.BlockHeight
    blocks_preload_pool_size: int

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        network: Network,
        aws_access_key_id: str,
        aws_secret_key: str,
        start_block_height: near_primitives.BlockHeight,
        preload_pool_size: None = None,
        block_preload_pool_size: int = 200,
    ):
        if preload_pool_size:
            logger.warning(
                "The 'preload_pool_size' argument is not used and will be deprecated in a "
                "future release. Use 'blocks_preload_pool_size' instead."
            )

        # These are entirely determined by Network.
        self.s3_bucket_name = f"near-lake-data-{network.value}"
        self.s3_region_name = "eu-central-1"

        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_key = aws_secret_key
        self.start_block_height = start_block_height
        self.blocks_preload_pool_size = block_preload_pool_size


async def start(config: LakeConfig, streamer_messages_queue: asyncio.Queue):
    session = get_session()
    async with session.create_client(
        "s3",
        region_name=config.s3_region_name,
        aws_secret_access_key=config.aws_secret_key,
        aws_access_key_id=config.aws_access_key_id,
    ) as s3_client:
        start_from_block_height: near_primitives.BlockHeight = config.start_block_height
        last_processed_block_hash: Optional[str] = None

        while True:
            block_heights_prefixes = await s3_fetchers.list_blocks(
                s3_client,
                config.s3_bucket_name,
                start_from_block_height,
                config.blocks_preload_pool_size * 2,
            )

            if not block_heights_prefixes:
                logger.info("No new blocks on S3, retry in 2s...")

                await asyncio.sleep(2)
                continue

            logger.info("Received %d blocks from S3", len(block_heights_prefixes))

            pending_block_heights = iter(block_heights_prefixes)
            streamer_messages_futures = []
            for block_height in itertools.islice(
                pending_block_heights, streamer_messages_queue.maxsize
            ):
                streamer_messages_futures.append(
                    asyncio.create_task(
                        s3_fetchers.fetch_streamer_message(
                            s3_client, config.s3_bucket_name, block_height
                        )
                    )
                )

            while streamer_messages_futures:
                streamer_message = await streamer_messages_futures.pop(0)

                if (
                    last_processed_block_hash
                    and last_processed_block_hash
                    != streamer_message.block.header.prev_hash
                ):
                    logger.warning(
                        "`prev_hash` does not match, re-fetching the data from S3 in 200ms: "
                        "%s != %s",
                        last_processed_block_hash,
                        streamer_message.block.header.prev_hash,
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
                        asyncio.create_task(
                            s3_fetchers.fetch_streamer_message(
                                s3_client,
                                config.s3_bucket_name,
                                pending_block_height,
                            )
                        )
                    )

                await streamer_messages_queue.put(streamer_message)


def streamer(config: LakeConfig):
    streamer_messages_queue: asyncio.Queue = asyncio.Queue(
        maxsize=config.blocks_preload_pool_size
    )
    stream_handle = asyncio.create_task(start(config, streamer_messages_queue))
    return stream_handle, streamer_messages_queue
