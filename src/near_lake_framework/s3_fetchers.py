import asyncio
from typing import List
import traceback

from near_lake_framework import near_primitives


async def list_blocks(
    s3_client,
    s3_bucket_name: str,
    start_from_block_height: near_primitives.BlockHeight,
    number_of_blocks_requested: int,
) -> List[near_primitives.BlockHeight]:
    response = await s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Delimiter="/",
        MaxKeys=number_of_blocks_requested,
        StartAfter="{:012d}".format(start_from_block_height),
        RequestPayer="requester",
    )

    return [
        near_primitives.BlockHeight(prefix.get("Prefix")[:-1])
        for prefix in response.get("CommonPrefixes", [])
    ]


async def fetch_streamer_message(
    s3_client, s3_bucket_name: str, block_height: near_primitives.BlockHeight
) -> near_primitives.StreamerMessage:
    response = await s3_client.get_object(
        Bucket=s3_bucket_name,
        Key="{:012d}/block.json".format(block_height),
        RequestPayer="requester",
    )

    async with response["Body"] as stream:
        body = await stream.read()

    block = near_primitives.Block.from_json(body)

    shards_fetching = [
        fetch_shard_or_retry(s3_client, s3_bucket_name, block_height, shard_id)
        for shard_id in range(len(block.chunks))
    ]
    shards = await asyncio.gather(*shards_fetching)

    return near_primitives.StreamerMessage(block, shards)


async def fetch_shard_or_retry(
    s3_client,
    s3_bucket_name: str,
    block_height: near_primitives.BlockHeight,
    shard_id: int,
) -> near_primitives.IndexerShard:
    while True:
        try:
            response = await s3_client.get_object(
                Bucket=s3_bucket_name,
                Key="{:012d}/shard_{}.json".format(block_height, shard_id),
                RequestPayer="requester",
            )

            async with response["Body"] as stream:
                body = await stream.read()

            return near_primitives.IndexerShard.from_json(body)
        except Exception:
            traceback.print_exc()
