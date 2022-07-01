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

    print(block_heights[-1])

    return block_heights


async def fetch_streamer_message(s3_client, s3_bucket_name: str, block_height):
    response = s3_client.get_object(
        Bucket=s3_bucket_name,
        Key="{:012d}/block.json".format(block_height),
        RequestPayer="requester",
    )


async def fetch_shard_or_retry(s3_client, s3_bucket_name: str, block_height, shard_id: int):
    pass


async def main():
    s3_client = boto3.client("s3")
    print(await list_blocks(s3_client, "near-lake-data-mainnet", 68875675, 10))

asyncio.run(main())
