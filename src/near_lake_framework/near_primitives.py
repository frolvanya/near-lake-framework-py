from typing import Any, List

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config, mm


@dataclass
class CryptoHash(DataClassJsonMixin):
    hash: Any


BlockHeight = int


class BlockHeightField(mm.fields.Integer):
    """Block Height is unsigned 64-bit integer, so it needs to be serialized as a string and get deserialized
    to an integer type in Python.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, as_string=True)


@dataclass
class BlockHeader(DataClassJsonMixin):
    height: BlockHeight = field(metadata=config(mm_field=BlockHeightField()))
    prev_height: BlockHeight = field(metadata=config(mm_field=BlockHeightField()))
    epoch_id: str
    next_epoch_id: str
    hash: str
    prev_hash: str
    prev_state_root: str
    chunk_receipts_root: str
    chunk_headers_root: str
    chunk_tx_root: str
    outcome_root: str
    chunks_included: int
    challenges_root: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    timestamp: int
    timestamp_nanosec: field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    random_value: str
    validator_proposals: List[Any]
    chunk_mask: List[bool]
    gas_price: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    block_ordinal: int
    rent_paid: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    validator_reward: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    total_supply: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    challenges_result: List[Any]
    last_final_block: str
    last_ds_final_block: str
    next_bp_hash: str
    block_merkle_root: str
    epoch_sync_data_hash: Any
    approvals: Any
    signature: str
    latest_protocol_version: int


@dataclass
class Block(DataClassJsonMixin):
    author: str
    header: BlockHeader
    chunks: Any


@dataclass
class Receipt(DataClassJsonMixin):
    predecessor_id: str
    receiver_id: str
    receipt_id: str
    receipt: Any


@dataclass
class ExecutionOutcome(DataClassJsonMixin):
    logs: List[str]
    receipt_ids: List[str]
    gas_burnt: int
    tokens_burnt: field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    executor_id: str
    status: Any
    metadata: Any


@dataclass
class ExecutionOutcomeWithId(DataClassJsonMixin):
    proof: List[Any]
    block_hash: str
    id: str
    outcome: ExecutionOutcome


@dataclass
class IndexerExecutionOutcomeWithReceipt(DataClassJsonMixin):
    execution_outcome: ExecutionOutcomeWithId
    receipt: Receipt


@dataclass
class IndexerShard(DataClassJsonMixin):
    shard_id: int
    chunk: List[str]
    receipt_execution_outcomes: List[IndexerExecutionOutcomeWithReceipt]
    state_changes: List[Any]


@dataclass
class StreamerMessage(DataClassJsonMixin):
    block: Block
    shards: List[IndexerShard]
