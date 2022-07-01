from typing import Annotated, Any, List

from dataclasses import dataclass
from typing_extensions import Self
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BlockHeight:
    block_height: int


@dataclass_json
@dataclass
class BlockView:
    author: str
    header: Any
    chunks: Any


@dataclass_json
@dataclass
class IndexerShard:
    shard_id: int
    chunk: List[Any]
    receipt_execution_outcomes: List[Any]
    state_changes: List[Any]


@dataclass_json
@dataclass
class StreamerMessage:
    block: BlockView
    shards: List[Any]


@dataclass
class LakeConfig:
    s3_bucket_name: str
    s3_region_name: str
    start_block_height: int

    def mainnet(self) -> Self:
        self.s3_bucket_name = "near-lake-data-mainnet"
        self.s3_region_name = "eu-central-1"

        return self

    def testnet(self) -> Self:
        self.s3_bucket_name = "near-lake-data-testnet"
        self.s3_region_name = "eu-central-1"

        return self
