from typing import Annotated, Any, List, Union

from dataclasses import dataclass
from typing_extensions import Self
from dataclasses_json import dataclass_json
from dataclasses_json import DataClassJsonMixin


@dataclass_json
@dataclass
class CryptoHash(DataClassJsonMixin):
    # hash: Annotated[List[int], 32]
    hash: Any


@dataclass_json
@dataclass
class BlockHeight(DataClassJsonMixin):
    block_height: int


@dataclass_json
@dataclass
class BlockHeaderView(DataClassJsonMixin):
    height: int
    prev_height: int
    epoch_id: Any
    next_epoch_id: Any
    hash: Any
    prev_hash: Any
    prev_state_root: Any
    chunk_receipts_root: Any
    chunk_headers_root: Any
    chunk_tx_root: Any
    outcome_root: Any
    chunks_included: int
    challenges_root: Any
    timestamp: int
    timestamp_nanosec: int
    random_value: Any
    validator_proposals: List[Any]
    chunk_mask: List[bool]
    gas_price: int
    block_ordinal: int
    rent_paid: int
    validator_reward: int
    total_supply: int
    challenges_result: List[Any]
    last_final_block: Any
    last_ds_final_block: Any
    next_bp_hash: Any
    block_merkle_root: Any
    epoch_sync_data_hash: Any
    # approvals: Union[str, None]
    approvals: Any
    signature: str
    latest_protocol_version: int


@dataclass_json
@dataclass
class BlockView(DataClassJsonMixin):
    author: str
    header: BlockHeaderView
    chunks: Any


@dataclass_json
@dataclass
class IndexerShard(DataClassJsonMixin):
    shard_id: int
    chunk: List[Any]
    receipt_execution_outcomes: List[Any]
    state_changes: List[Any]


@dataclass_json
@dataclass
class StreamerMessage(DataClassJsonMixin):
    block: BlockView
    shards: List[Any]


@dataclass
class LakeConfig:
    s3_bucket_name: str
    s3_region_name: str
    start_block_height: int
    blocks_preload_pool_size: int

    def mainnet(self) -> Self:
        self.s3_bucket_name = "near-lake-data-mainnet"
        self.s3_region_name = "eu-central-1"

        return self

    def testnet(self) -> Self:
        self.s3_bucket_name = "near-lake-data-testnet"
        self.s3_region_name = "eu-central-1"

        return self
