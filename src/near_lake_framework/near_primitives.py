from typing import Any, List, Optional

from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin, config, mm


AccountId = str
CryptoHash = str
BlockHeight = int


class BlockHeightField(mm.fields.Integer):
    """Block Height is unsigned 64-bit integer, so it needs to be serialized as a string and get deserialized
    to an integer type in Python.
    """

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs, as_string=True)


@dataclass
class BlockHeader(DataClassJsonMixin):
    epoch_id: CryptoHash
    next_epoch_id: CryptoHash
    hash: CryptoHash
    prev_hash: CryptoHash
    prev_state_root: CryptoHash
    chunk_receipts_root: CryptoHash
    chunk_headers_root: CryptoHash
    chunk_tx_root: CryptoHash
    outcome_root: CryptoHash
    chunks_included: int
    challenges_root: CryptoHash
    timestamp: int
    timestamp_nanosec: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    random_value: CryptoHash
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
    last_final_block: CryptoHash
    last_ds_final_block: CryptoHash
    next_bp_hash: CryptoHash
    block_merkle_root: CryptoHash
    epoch_sync_data_hash: Optional[CryptoHash]
    approvals: List[Optional[str]]
    signature: str
    latest_protocol_version: int
    height: BlockHeight = field(metadata=config(mm_field=BlockHeightField()))
    prev_height: Optional[BlockHeight] = field(
        default=None, metadata=config(mm_field=BlockHeightField())
    )


@dataclass
class ChunkHeader(DataClassJsonMixin):
    chunk_hash: CryptoHash
    prev_block_hash: CryptoHash
    outcome_root: CryptoHash
    prev_state_root: CryptoHash
    encoded_merkle_root: CryptoHash
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
    outgoing_receipts_root: CryptoHash
    tx_root: CryptoHash
    validator_proposals: List[Any]
    signature: str


@dataclass
class Block(DataClassJsonMixin):
    author: AccountId
    header: BlockHeader
    chunks: List[ChunkHeader]


@dataclass
class Receipt(DataClassJsonMixin):
    predecessor_id: AccountId
    receiver_id: AccountId
    receipt_id: CryptoHash
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
    receipt_ids: List[CryptoHash]
    gas_burnt: int
    tokens_burnt: int = field(
        metadata=config(mm_field=mm.fields.Integer(as_string=True))
    )
    executor_id: AccountId
    status: Any
    metadata: ExecutionMetadata


@dataclass
class ExecutionOutcomeWithId(DataClassJsonMixin):
    proof: List[Any]
    block_hash: CryptoHash
    id: CryptoHash
    outcome: ExecutionOutcome


@dataclass
class IndexerExecutionOutcomeWithReceipt(DataClassJsonMixin):
    execution_outcome: ExecutionOutcomeWithId
    receipt: Receipt


@dataclass
class SignedTransaction(DataClassJsonMixin):
    signer_id: AccountId
    public_key: str
    nonce: int
    receiver_id: AccountId
    actions: List[Any]
    signature: str
    hash: CryptoHash


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
    author: AccountId
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
