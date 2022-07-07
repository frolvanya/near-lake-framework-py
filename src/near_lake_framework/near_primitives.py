from typing import Annotated, Any, List, Union
from typing_extensions import TypeAlias

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, dataclass_json, config, mm


@dataclass_json
@dataclass
class CryptoHash:
    hash: Any


BlockHeight = int


class BlockHeightField(mm.fields.Integer):
    """Block Height is unsigned 64-bit integer, so it needs to be serialized as a string and get deserialized
    to an integer type in Python.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, as_string=True)


@dataclass_json
@dataclass
class BlockHeaderView:
    height: BlockHeight = field(metadata=config(mm_field=BlockHeightField()))
    prev_height: BlockHeight = field(
        metadata=config(mm_field=BlockHeightField()))
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
class StreamerMessage:
    block: BlockView
    shards: List[Any]
