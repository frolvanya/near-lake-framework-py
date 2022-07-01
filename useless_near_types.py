from typing import Annotated, Any, List, Union

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BlockHeight:
    block_height: int

    def __int__(self):
        return self.block_height

    def __str__(self):
        return str(self.block_height)


@dataclass_json
@dataclass
class CryptoHash:
    hash: Annotated[List[int], 32]


@dataclass_json
@dataclass
class ValidatorStakeView:
    account_id: str
    public_key: str
    stake: int
    # public_key: PublicKey


@dataclass_json
@dataclass
class SlashedValidator:
    account_id: str
    is_double_sign: bool


@dataclass_json
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


@dataclass_json
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


@dataclass_json
@dataclass
class AccessKeyPermissionView:
    @dataclass_json
    @dataclass
    class FunctionCall:
        allowance: int
        receiver_id: str
        method_names: List[str]

    @dataclass_json
    @dataclass
    class FullAccess:
        pass


@dataclass_json
@dataclass
class AccessKeyView:
    nonce: int
    permission: AccessKeyPermissionView


@dataclass_json
@dataclass
class ActionView:
    @dataclass_json
    @dataclass
    class CreateAccount:
        pass

    @dataclass_json
    @dataclass
    class DeployContract:
        code: str

    @dataclass_json
    @dataclass
    class FunctionCall:
        method_name: str
        args: str
        gas: int
        deposit: int

    @dataclass_json
    @dataclass
    class Transfer:
        deposit: int

    @dataclass_json
    @dataclass
    class Stake:
        stake: int
        public_key: str

    @dataclass_json
    @dataclass
    class AddKey:
        public_key: str
        access_key: AccessKeyView

    @dataclass_json
    @dataclass
    class DeleteKey:
        public_key: str

    @dataclass_json
    @dataclass
    class DeleteAccount:
        beneficiary_id: str


@dataclass_json
@dataclass
class SignedTransactionView:
    signer_id: str
    public_key: str
    nonce: int
    receiver_id: str
    actions: List[ActionView]
    signature: str
    hash: CryptoHash


@dataclass_json
@dataclass
class Direction:
    @dataclass_json
    @dataclass
    class Left:
        pass

    @dataclass_json
    @dataclass
    class Right:
        pass


@dataclass_json
@dataclass
class MerklePathItem:
    hash: CryptoHash
    direction: Direction


@dataclass_json
@dataclass
class ExecutionStatusView:
    @dataclass_json
    @dataclass
    class Unknown:
        pass

    @dataclass_json
    @dataclass
    class Failure:
        pass

    @dataclass_json
    @dataclass
    class SuccessValue:
        value: str

    @dataclass_json
    @dataclass
    class SuccessReceiptId:
        receipt_id: CryptoHash


@dataclass_json
@dataclass
class CostGasUsed:
    cost_category: str
    cost: str
    gas_used: int


@dataclass_json
@dataclass
class ExecutionMetadataView:
    version: int
    gas_profile: List[CostGasUsed]


@dataclass_json
@dataclass
class ExecutionOutcomeView:
    logs: List[str]
    receipt_ids: List[CryptoHash]
    gas_burnt: int
    tokens_burnt: int
    executor_id: str
    status: ExecutionStatusView
    metadata: ExecutionMetadataView


@dataclass_json
@dataclass
class ExecutionOutcomeWithIdView:
    proof: List[MerklePathItem]
    block_hash: CryptoHash
    id: CryptoHash
    outcome: ExecutionOutcomeView


@dataclass_json
@dataclass
class DataReceiverView:
    data_id: CryptoHash
    receiver_id: str


@dataclass_json
@dataclass
class ReceiptEnumView:
    @dataclass_json
    @dataclass
    class Action:
        signer_id: str
        signer_public_key: str
        gas_price: int
        output_data_receivers: List[DataReceiverView]
        input_data_ids: List[CryptoHash]
        actions: List[ActionView]

    @dataclass_json
    @dataclass
    class Data:
        data_id: CryptoHash
        data: List[int]


@dataclass_json
@dataclass
class ReceiptView:
    predecessor_id: str
    receiver_id: str
    receipt_id: CryptoHash
    receipt: ReceiptEnumView


@dataclass_json
@dataclass
class IndexerExecutionOutcomeWithOptionalReceipt:
    execution_outcome: ExecutionOutcomeWithIdView
    receipt: ReceiptView


@dataclass_json
@dataclass
class IndexerTransactionWithOutcome:
    transaction: SignedTransactionView
    outcome: IndexerExecutionOutcomeWithOptionalReceipt
    # public_key: PublicKey,
    # signature: Signature
    # self.actions = actions


@dataclass_json
@dataclass
class IndexerChunkView:
    author: str
    header: ChunkHeaderView
    transactions: List[IndexerTransactionWithOutcome]
    receipts: List[ReceiptView]


# @dataclass_json
# @dataclass
# class BlockView:
#     author: str
#     header: BlockHeaderView
#     chunks: ChunkHeaderView

@dataclass_json
@dataclass
class BlockView:
    author: str
    header: Any
    chunks: Any


@dataclass_json
@dataclass
class IndexerExecutionOutcomeWithReceipt:
    execution_outcome: ExecutionOutcomeWithIdView
    receipt: ReceiptView


@dataclass_json
@dataclass
class StateChangeCauseView:
    @dataclass_json
    @dataclass
    class NotWritableToDisk:
        pass

    @dataclass_json
    @dataclass
    class InitialState:
        pass

    @dataclass_json
    @dataclass
    class TransactionProcessing:
        tx_hash: CryptoHash

    @dataclass_json
    @dataclass
    class ActionReceiptProcessingStarted:
        receipt_hash: CryptoHash

    @dataclass_json
    @dataclass
    class ActionReceiptGasReward:
        receipt_hash: CryptoHash

    @dataclass_json
    @dataclass
    class ReceiptProcessing:
        receipt_hash: CryptoHash

    @dataclass_json
    @dataclass
    class PostponedReceipt:
        receipt_hash: CryptoHash

    @dataclass_json
    @dataclass
    class UpdatedDelayedReceipts:
        pass

    @dataclass_json
    @dataclass
    class ValidatorAccountsUpdate:
        pass

    @dataclass_json
    @dataclass
    class Migration:
        pass

    @dataclass_json
    @dataclass
    class Resharding:
        pass


@dataclass_json
@dataclass
class AccountView:
    amount: int
    locked: int
    code_hash: CryptoHash
    storage_usage: int
    storage_paid_at: int


@dataclass_json
@dataclass
class StateChangeValueView:
    @dataclass_json
    @dataclass
    class AccountUpdate:
        account_id: str
        account: AccountView

    @dataclass_json
    @dataclass
    class AccountDeletion:
        account_id: str

    @dataclass_json
    @dataclass
    class AccessKeyUpdate:
        account_id: str
        public_key: str
        access_key: AccessKeyView

    @dataclass_json
    @dataclass
    class AccessKeyDeletion:
        account_id: str
        public_key: str

    @dataclass_json
    @dataclass
    class DataUpdate:
        account_id: str
        key: str
        value: str

    @dataclass_json
    @dataclass
    class DataDeletion:
        account_id: str
        key: str

    @dataclass_json
    @dataclass
    class ContractCodeUpdate:
        account_id: str
        code: List[int]

    @dataclass_json
    @dataclass
    class ContractCodeDeletion:
        account_id: str


@dataclass_json
@dataclass
class StateChangeWithCauseView:
    cause: StateChangeCauseView
    value: StateChangeValueView


@dataclass_json
@dataclass
class IndexerShard:
    shard_id: int
    chunk: List[IndexerChunkView]
    receipt_execution_outcomes: List[IndexerExecutionOutcomeWithReceipt]
    state_changes: List[StateChangeWithCauseView]


@dataclass_json
@dataclass
class StreamerMessage:
    block: BlockView
    shards: List[IndexerShard]
