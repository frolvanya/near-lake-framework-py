import asyncio
import logging
import traceback
from botocore.exceptions import ClientError, EndpointConnectionError

from near_lake_framework import near_primitives


async def list_blocks(
    s3_client,
    s3_bucket_name: str,
    start_from_block_height: near_primitives.BlockHeight,
    number_of_blocks_requested: int,
) -> list[near_primitives.BlockHeight]:
    response = await s3_client.list_objects_v2(
        Bucket=s3_bucket_name,
        Delimiter="/",
        MaxKeys=number_of_blocks_requested,
        StartAfter=f"{start_from_block_height:012d}",
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
        Key=f"{block_height:012d}/block.json",
        RequestPayer="requester",
    )

    async with response["Body"] as stream:
        body = await stream.read()

    block = near_primitives.Block.from_json(body)

    shards_fetching = [
        fetch_shard_or_retry(s3_client, s3_bucket_name, block_height, chunk.shard_id)
        for chunk in block.chunks
    ]
    shards = await asyncio.gather(*shards_fetching)

    return near_primitives.StreamerMessage(block, list(shards))


async def fetch_shard_or_retry(
    s3_client,
    s3_bucket_name: str,
    block_height: near_primitives.BlockHeight,
    shard_id: int,
) -> near_primitives.IndexerShard:
    while True:
        shard_key = f"{block_height:012d}/shard_{shard_id}.json"
        try:
            response = await s3_client.get_object(
                Bucket=s3_bucket_name,
                Key=shard_key,
                RequestPayer="requester",
            )

            async with response["Body"] as stream:
                body = await stream.read()

            return near_primitives.IndexerShard.from_json(body)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                logging.debug("Failed to fetch shard %s - doesn't exist", shard_key)
            else:
                traceback.print_exc()
        except EndpointConnectionError as e:
            logging.error(
                "EndpointConnectionError while fetching shard %s: %s", shard_key, e
            )
            traceback.print_exc()
        except asyncio.TimeoutError as e:
            logging.error("TimeoutError while fetching shard %s: %s", shard_key, e)
            traceback.print_exc()
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error("Unexpected error while fetching shard %s: %s", shard_key, e)
            traceback.print_exc()
