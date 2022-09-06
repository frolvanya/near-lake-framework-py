# NEAR Lake Framework for Python

Available in programming languages: [Rust](https://github.com/near/near-lake-framework-rs) | [Javascript](https://github.com/near/near-lake-framework-js) | **Python3**

NEAR Lake Framework is a small library companion to [NEAR Lake](https://github.com/near/near-lake). It allows you to build
your own indexer that subscribes to the stream of blocks from the NEAR Lake data source and create your own logic to process
the NEAR Protocol data.

[![PyPI version](https://badge.fury.io/py/near-lake-framework.svg)](https://badge.fury.io/py/near-lake-framework)
![MIT or Apache 2.0 licensed](https://img.shields.io/crates/l/near-lake-framework.svg)

---

[Official NEAR Lake Framework launch announcement](https://gov.near.org/t/announcement-near-lake-framework-brand-new-word-in-indexer-building-approach/17668) has been published on the NEAR Gov Forum
Greetings from the Data Platform Team! We are happy and proud to announce an MVP release of a brand new word in indexer building approach - NEAR Lake Framework.

---

## Example

```python3
import asyncio
import os

from near_lake_framework import LakeConfig, streamer


async def main():
    config = LakeConfig.mainnet()
    config.start_block_height = 69130938
    config.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    config.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    stream_handle, streamer_messages_queue = streamer(config)
    while True:
        streamer_message = await streamer_messages_queue.get()
        print(
            f"Received Block #{streamer_message.block.header.height} from Lake Framework"
        )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

## How to use

### Dependencies

Install `near-lake-framework`

```bash
$ pip3 install near-lake-framework
```

### Credentials

To be able to access the data from NEAR Lake you need to provide credentials. Please, see the [Credentials article](https://near-indexers.io/tutorials/lake/credentials)

## Configuration

Everything should be configured before the start of your indexer application via `LakeConfig` struct.

Available parameters:

- `s3_bucket_name: str` - provide the AWS S3 bucket name (`near-lake-testnet`, `near-lake-mainnet` or yours if you run your own NEAR Lake)
- `s3_region_name: str` - provide the region for AWS S3 bucket
- `start_block_height: BlockHeight` - block height to start the stream from
- `blocks_preload_pool_size: int` - provide the number of blocks to preload (default: 200)

## Cost estimates

**TL;DR** approximately $18.15 per month (for AWS S3 access, paid directly to AWS) for the reading of fresh blocks

Explanation:

Assuming NEAR Protocol produces accurately 1 block per second (which is really not, the average block production time is 1.3s). A full day consists of 86400 seconds, that's the max number of blocks that can be produced.

According the [Amazon S3 prices](https://aws.amazon.com/s3/pricing/?nc1=h_ls) `list` requests are charged for $0.005 per 1000 requests and `get` is charged for $0.0004 per 1000 requests.

Calculations (assuming we are following the tip of the network all the time):

```
86400 blocks per day * 5 requests for each block / 1000 requests * $0.0004 per 1k requests = $0.173 * 30 days = $5.19
```
**Note:** 5 requests for each block means we have 4 shards (1 file for common block data and 4 separate files for each shard)

And a number of `list` requests we need to perform for 30 days:

```
86400 blocks per day / 1000 requests * $0.005 per 1k list requests = $0.432 * 30 days = $12.96

$5.19 + $12.96 = $18.15
```

The price depends on the number of shards


### Publishing to PyPi

[Follow this guide to safely publish PyPi package](https://widdowquinn.github.io/coding/update-pypi-package/)
