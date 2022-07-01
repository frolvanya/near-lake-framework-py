from typing import Annotated, List, Union
from dataclasses import dataclass


@dataclass
class BlockHeight:
    block_height: int

    def __int__(self):
        return self.block_height

    def __str__(self):
        return str(self.block_height)


@dataclass
class CryptoHash:
    hash: Annotated[List[int], 32]


@dataclass
class ValidatorStakeView:
    account_id: str
    public_key: str
    stake: int
    # public_key: PublicKey


@dataclass
class SlashedValidator:
    account_id: str
    is_double_sign: bool


@dataclass
class BlockHeaderView:
    height: int
    prev_height: int
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
    timestamp_nanosec: int
    random_value: CryptoHash
    validator_proposals: List[ValidatorStakeView]
    chunk_mask: List[bool]
    gas_price: int
    block_ordinal: int
    rent_paid: int
    validator_reward: int
    total_supply: int
    challenges_result: List[SlashedValidator]
    last_final_block: CryptoHash
    last_ds_final_block: CryptoHash
    next_bp_hash: CryptoHash
    block_merkle_root: CryptoHash
    epoch_sync_data_hash: CryptoHash
    approvals: Union[str, None]
    signature: str
    latest_protocol_version: int

    #   approvals: Vec < Option < Signature > , Global > ,
    #   signature: Signature,


@dataclass
class ChunkHeaderView:
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
    rent_paid: int
    validator_reward: int
    balance_burnt: int
    outgoing_receipts_root: CryptoHash
    tx_root: CryptoHash
    validator_proposals: List[ValidatorStakeView]
    signature: str
    # signature: Signature,


@dataclass
class AccessKeyPermissionView:
    @dataclass
    class FunctionCall:
        allowance: int
        receiver_id: str
        method_names: List[str]

    @dataclass
    class FullAccess:
        pass


@dataclass
class AccessKeyView:
    nonce: int
    permission: AccessKeyPermissionView


@dataclass
class ActionView:
    @dataclass
    class CreateAccount:
        pass

    @dataclass
    class DeployContract:
        code: str

    @dataclass
    class FunctionCall:
        method_name: str
        args: str
        gas: int
        deposit: int

    @dataclass
    class Transfer:
        deposit: int

    @dataclass
    class Stake:
        stake: int
        public_key: str

    @dataclass
    class AddKey:
        public_key: str
        access_key: AccessKeyView

    @dataclass
    class DeleteKey:
        public_key: str

    @dataclass
    class DeleteAccount:
        beneficiary_id: str


@dataclass
class SignedTransactionView:
    signer_id: str
    public_key: str
    nonce: int
    receiver_id: str
    actions: List[ActionView]
    signature: str
    hash: CryptoHash


@dataclass
class Direction:
    @dataclass
    class Left:
        pass

    @dataclass
    class Right:
        pass


@dataclass
class MerklePathItem:
    hash: CryptoHash
    direction: Direction


@dataclass
class ExecutionStatusView:
    @dataclass
    class Unknown:
        pass

    @dataclass
    class Failure:
        pass

    @dataclass
    class SuccessValue:
        value: str

    @dataclass
    class SuccessReceiptId:
        receipt_id: CryptoHash


@dataclass
class CostGasUsed:
    cost_category: str
    cost: str
    gas_used: int


@dataclass
class ExecutionMetadataView:
    version: int
    gas_profile: List[CostGasUsed]


@dataclass
class ExecutionOutcomeView:
    logs: List[str]
    receipt_ids: List[CryptoHash]
    gas_burnt: int
    tokens_burnt: int
    executor_id: str
    status: ExecutionStatusView
    metadata: ExecutionMetadataView


@dataclass
class ExecutionOutcomeWithIdView:
    proof: List[MerklePathItem]
    block_hash: CryptoHash
    id: CryptoHash
    outcome: ExecutionOutcomeView


@dataclass
class DataReceiverView:
    data_id: CryptoHash
    receiver_id: str


@dataclass
class ReceiptEnumView:
    @dataclass
    class Action:
        signer_id: str
        signer_public_key: str
        gas_price: int
        output_data_receivers: List[DataReceiverView]
        input_data_ids: List[CryptoHash]
        actions: List[ActionView]

    @dataclass
    class Data:
        data_id: CryptoHash
        data: List[int]


@dataclass
class ReceiptView:
    predecessor_id: str
    receiver_id: str
    receipt_id: CryptoHash
    receipt: ReceiptEnumView


@dataclass
class IndexerExecutionOutcomeWithOptionalReceipt:
    execution_outcome: ExecutionOutcomeWithIdView
    receipt: ReceiptView


@dataclass
class IndexerTransactionWithOutcome:
    transaction: SignedTransactionView
    outcome: IndexerExecutionOutcomeWithOptionalReceipt
    # public_key: PublicKey,
    # signature: Signature
    # self.actions = actions


@dataclass
class IndexerChunkView:
    author: str
    header: ChunkHeaderView
    transactions: List[IndexerTransactionWithOutcome]
    receipts: List[ReceiptView]


@dataclass
class BlockView:
    author: str
    header: BlockHeaderView
    chunks: ChunkHeaderView


@dataclass
class IndexerExecutionOutcomeWithReceipt:
    execution_outcome: ExecutionOutcomeWithIdView
    receipt: ReceiptView


@dataclass
class StateChangeCauseView:
    @dataclass
    class NotWritableToDisk:
        pass

    @dataclass
    class InitialState:
        pass

    @dataclass
    class TransactionProcessing:
        tx_hash: CryptoHash

    @dataclass
    class ActionReceiptProcessingStarted:
        receipt_hash: CryptoHash

    @dataclass
    class ActionReceiptGasReward:
        receipt_hash: CryptoHash

    @dataclass
    class ReceiptProcessing:
        receipt_hash: CryptoHash

    @dataclass
    class PostponedReceipt:
        receipt_hash: CryptoHash

    @dataclass
    class UpdatedDelayedReceipts:
        pass

    @dataclass
    class ValidatorAccountsUpdate:
        pass

    @dataclass
    class Migration:
        pass

    @dataclass
    class Resharding:
        pass


@dataclass
class AccountView:
    amount: int
    locked: int
    code_hash: CryptoHash
    storage_usage: int
    storage_paid_at: int


@dataclass
class StateChangeValueView:
    @dataclass
    class AccountUpdate:
        account_id: str
        account: AccountView

    @dataclass
    class AccountDeletion:
        account_id: str

    @dataclass
    class AccessKeyUpdate:
        account_id: str
        public_key: str
        access_key: AccessKeyView

    @dataclass
    class AccessKeyDeletion:
        account_id: str
        public_key: str

    @dataclass
    class DataUpdate:
        account_id: str
        key: str
        value: str

    @dataclass
    class DataDeletion:
        account_id: str
        key: str

    @dataclass
    class ContractCodeUpdate:
        account_id: str
        code: List[int]

    @dataclass
    class ContractCodeDeletion:
        account_id: str


@dataclass
class StateChangeWithCauseView:
    cause: StateChangeCauseView
    value: StateChangeValueView


@dataclass
class IndexerShard:
    shard_id: int
    chunk: List[IndexerChunkView]
    receipt_execution_outcomes: List[IndexerExecutionOutcomeWithReceipt]
    state_changes: List[StateChangeWithCauseView]


@dataclass
class StreamerMessage:
    block: BlockView
    shards: List[IndexerShard]
