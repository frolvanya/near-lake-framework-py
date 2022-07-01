import json
from typing import List
import boto3
import asyncio

import near_types

ESTIMATED_SHARDS_COUNT = 4


async def list_blocks(s3_client, s3_bucket_name: str, start_from_block_height: near_types.BlockHeight, number_of_blocks_requested: int) -> List[near_types.BlockHeight]:
    response = s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Delimiter="/",
        MaxKeys=number_of_blocks_requested * (1 + ESTIMATED_SHARDS_COUNT),
        StartAfter="{:012d}".format(start_from_block_height),
        RequestPayer="requester",
    )

    block_heights = []

    for prefix in response.get('CommonPrefixes'):
        block_heights.append(near_types.BlockHeight(
            int(prefix.get('Prefix')[:-1])))

    return block_heights


async def fetch_streamer_message(s3_client, s3_bucket_name: str, block_height: near_types.BlockHeight) -> near_types.StreamerMessage:
    response = s3_client.get_object(
        Bucket=s3_bucket_name,
        Key="{:012d}/block.json".format(block_height),
        RequestPayer="requester",
    )

    json_content = json.loads(response['Body'].read().decode('utf-8'))

    block_view = near_types.BlockView.from_dict(json_content)
    # shards = await asyncio.gather(*[fetch_shard_or_retry(s3_client, s3_bucket_name, block_height, shard_id) for shard_id in range(len(block_view.chunks))])

    shards_fetching = [
        fetch_shard_or_retry(s3_client, s3_bucket_name, block_height, shard_id)
        for shard_id in range(len(block_view.chunks))
    ]
    shards = await asyncio.gather(*shards_fetching)

    return near_types.StreamerMessage(block_view, shards)


async def fetch_shard_or_retry(s3_client, s3_bucket_name: str, block_height: near_types.BlockHeight, shard_id: int) -> near_types.IndexerShard:
    response = s3_client.get_object(
        Bucket=s3_bucket_name,
        Key="{:012d}/shard_{}.json".format(block_height, shard_id),
        RequestPayer="requester",
    )

    json_content = json.loads(response['Body'].read().decode('utf-8'))
    return near_types.IndexerShard.from_dict(json_content)


async def main():
    s3_client = boto3.client("s3")
    # print(await list_blocks(s3_client, "near-lake-data-mainnet", 68914412, 100))
    print(await fetch_streamer_message(s3_client, "near-lake-data-mainnet", 68914412))
    # print(await fetch_shard_or_retry(s3_client, "near-lake-data-mainnet", 68914412, 3))

asyncio.run(main())
