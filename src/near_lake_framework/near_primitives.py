from typing import Any, List, Optional

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
    challenges_root: str
    timestamp: int
    timestamp_nanosec: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    random_value: str
    validator_proposals: List[Any]
    chunk_mask: List[bool]
    gas_price: int = field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    block_ordinal: Optional[int]
    rent_paid: int = field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    validator_reward: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    total_supply: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    challenges_result: List[Any]
    last_final_block: str
    last_ds_final_block: str
    next_bp_hash: str
    block_merkle_root: str
    epoch_sync_data_hash: Optional[str]
    approvals: List[Optional[str]]
    signature: str
    latest_protocol_version: int


@dataclass
class ChunkHeader(DataClassJsonMixin):
    chunk_hash: str
    prev_block_hash: str
    outcome_root: str
    prev_state_root: str
    encoded_merkle_root: str
    encoded_length: int
    height_created: int
    height_included: int
    shard_id: int
    gas_used: int
    gas_limit: int
    rent_paid: int = field(metadata=config(mm_field=mm.fields.Integer(as_string=True)))
    validator_reward: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    balance_burnt: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    outgoing_receipts_root: str
    tx_root: str
    validator_proposals: List[Any]
    signature: str


@dataclass
class Block(DataClassJsonMixin):
    author: str
    header: BlockHeader
    chunks: List[ChunkHeader]


@dataclass
class Receipt(DataClassJsonMixin):
    predecessor_id: str
    receiver_id: str
    receipt_id: str
    receipt: Any


@dataclass
class CostGasUsed(DataClassJsonMixin):
    cost_category: str
    cost: str
    gas_used: int


@dataclass
class ExecutionMetadata(DataClassJsonMixin):
    version: int
    gas_profile: Optional[List[CostGasUsed]]


@dataclass
class ExecutionOutcome(DataClassJsonMixin):
    logs: List[str]
    receipt_ids: List[str]
    gas_burnt: int
    tokens_burnt: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    executor_id: str
    status: Any
    metadata: ExecutionMetadata


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
class SignedTransaction(DataClassJsonMixin):
    signer_id: str
    public_key: str
    nonce: int
    receiver_id: str
    actions: List[Any]
    signature: str
    hash: str


@dataclass
class IndexerExecutionOutcomeWithOptionalReceipt:
    execution_outcome: ExecutionOutcomeWithId
    receipt: Optional[Receipt]


@dataclass
class IndexerTransactionWithOutcome(DataClassJsonMixin):
    transaction: SignedTransaction
    outcome: IndexerExecutionOutcomeWithOptionalReceipt


@dataclass
class IndexerChunk(DataClassJsonMixin):
    author: str
    header: ChunkHeader
    transactions: List[IndexerTransactionWithOutcome]
    receipts: List[Receipt]


@dataclass
class IndexerShard(DataClassJsonMixin):
    shard_id: int
    chunk: Optional[IndexerChunk]
    receipt_execution_outcomes: List[IndexerExecutionOutcomeWithReceipt]
    state_changes: List[Any]


@dataclass
class StreamerMessage(DataClassJsonMixin):
    block: Block
    shards: List[IndexerShard]
