from aiobotocore.session import get_session
import asyncio

import json
from typing import List

import near_types

ESTIMATED_SHARDS_COUNT = 4

AWS_ACCESS_KEY_ID = "xxx"
AWS_SECRET_ACCESS_KEY = "xxx"
REGION_NAME = "xxx"


async def list_blocks(s3_bucket_name: str, start_from_block_height: near_types.BlockHeight, number_of_blocks_requested: int) -> List[near_types.BlockHeight]:
    session = get_session()
    async with session.create_client("s3", region_name=REGION_NAME,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                     aws_access_key_id=AWS_ACCESS_KEY_ID) as s3_client:
        paginator = s3_client.get_paginator("list_objects_v2")
        async for response in paginator.paginate(
            Bucket=s3_bucket_name,
            Delimiter="/",
            MaxKeys=number_of_blocks_requested * (1 + ESTIMATED_SHARDS_COUNT),
            StartAfter="{:012d}".format(start_from_block_height),
            RequestPayer="requester",
        ):
            block_heights = []

            for prefix in response.get("CommonPrefixes"):
                block_heights.append(near_types.BlockHeight(
                    int(prefix.get("Prefix")[:-1])))

    return block_heights


async def fetch_streamer_message(s3_bucket_name: str, block_height: near_types.BlockHeight) -> near_types.StreamerMessage:
    session = get_session()
    async with session.create_client("s3", region_name=REGION_NAME,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                     aws_access_key_id=AWS_ACCESS_KEY_ID) as s3_client:
        response = await s3_client.get_object(
            Bucket=s3_bucket_name,
            Key="{:012d}/block.json".format(block_height),
            RequestPayer="requester"
        )

        async with response["Body"] as stream:
            body = await stream.read()

    json_content = json.loads(body.decode("utf-8"))
    block_view = near_types.BlockView.from_dict(json_content)

    shards_fetching = [
        fetch_shard_or_retry(s3_bucket_name, block_height, shard_id)
        for shard_id in range(len(block_view.chunks))
    ]
    shards = await asyncio.gather(*shards_fetching)

    return near_types.StreamerMessage(block_view, shards)


async def fetch_shard_or_retry(s3_bucket_name: str, block_height: near_types.BlockHeight, shard_id: int) -> near_types.IndexerShard:
    session = get_session()
    async with session.create_client("s3", region_name=REGION_NAME,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                     aws_access_key_id=AWS_ACCESS_KEY_ID) as s3_client:
        response = await s3_client.get_object(
            Bucket=s3_bucket_name,
            Key="{:012d}/shard_{}.json".format(block_height, shard_id),
            RequestPayer="requester"
        )

        async with response["Body"] as stream:
            body = await stream.read()

    json_content = json.loads(body.decode("utf-8"))
    return near_types.IndexerShard.from_dict(json_content)


# async def main():
#     print(await list_blocks("near-lake-data-mainnet", 68914412, 10))
#     print(await fetch_streamer_message("near-lake-data-mainnet", 68914412))
#     print(await fetch_shard_or_retry("near-lake-data-mainnet", 68914412, 3))

# asyncio.run(main())
