from typing import Annotated, List


class BlockHeight:
    def __init__(self, block_height: int):
        self.block_height = block_height

    def __int__(self):
        return self.block_height

    def __str__(self):
        return str(self.block_height)


class CryptoHash:
    def __init__(self, hash: Annotated[List[int], 32]):
        self.hash = hash


class ValidatorStakeView:
    def __init__(self, account_id: str, public_key, stake: int):
        # public_key: PublicKey

        self.account_id = account_id
        self.public_key = public_key
        self.stake = stake


class SlashedValidator:
    def __init__(self, account_id: str, is_double_sign: bool):
        self.account_id = account_id
        self.is_double_sign = is_double_sign


class BlockHeaderView:
    def __init__(
        self,
        height: int,
        prev_height: int,
        epoch_id: CryptoHash,
        next_epoch_id: CryptoHash,
        hash: CryptoHash,
        prev_hash: CryptoHash,
        prev_state_root: CryptoHash,
        chunk_receipts_root: CryptoHash,
        chunk_headers_root: CryptoHash,
        chunk_tx_root: CryptoHash,
        outcome_root: CryptoHash,
        chunks_included: int,
        challenges_root: CryptoHash,
        timestamp: int,
        timestamp_nanosec: int,
        random_value: CryptoHash,
        validator_proposals: List[ValidatorStakeView],
        chunk_mask: List[bool],
        gas_price: int,
        block_ordinal: int,
        rent_paid: int,
        validator_reward: int,
        total_supply: int,
        challenges_result: List[SlashedValidator],
        last_final_block: CryptoHash,
        last_ds_final_block: CryptoHash,
        next_bp_hash: CryptoHash,
        block_merkle_root: CryptoHash,
        epoch_sync_data_hash: CryptoHash,
        approvals,
        signature,
        latest_protocol_version: int
    ):
        #   approvals: Vec < Option < Signature > , Global > ,
        #   signature: Signature,

        self.height = height
        self.prev_height = prev_height
        self.epoch_id = epoch_id
        self.next_epoch_id = next_epoch_id
        self.hash = hash
        self.prev_hash = prev_hash
        self.prev_state_root = prev_state_root
        self.chunk_receipts_root = chunk_receipts_root
        self.chunk_headers_root = chunk_headers_root
        self.chunk_tx_root = chunk_tx_root
        self.outcome_root = outcome_root
        self.chunks_included = chunks_included
        self.challenges_root = challenges_root
        self.timestamp = timestamp
        self.timestamp_nanosec = timestamp_nanosec
        self.random_value = random_value
        self.validator_proposals = validator_proposals
        self.chunk_mask = chunk_mask
        self.gas_price = gas_price
        self.block_ordinal = block_ordinal
        self.rent_paid = rent_paid
        self.validator_reward = validator_reward
        self.total_supply = total_supply
        self.challenges_result = challenges_result
        self.last_final_block = last_final_block
        self.last_ds_final_block = last_ds_final_block
        self.next_bp_hash = next_bp_hash
        self.block_merkle_root = block_merkle_root
        self.epoch_sync_data_hash = epoch_sync_data_hash
        self.approvals = approvals
        self.signature = signature
        self.latest_protocol_version = latest_protocol_version


class ChunkHeaderView:
    def __init__(
        self,
        chunk_hash: CryptoHash,
        prev_block_hash: CryptoHash,
        outcome_root: CryptoHash,
        prev_state_root: CryptoHash,
        encoded_merkle_root: CryptoHash,
        encoded_length: int,
        height_created: int,
        height_included: int,
        shard_id: int,
        gas_used: int,
        gas_limit: int,
        rent_paid: int,
        validator_reward: int,
        balance_burnt: int,
        outgoing_receipts_root: CryptoHash,
        tx_root: CryptoHash,
        validator_proposals: List[ValidatorStakeView],
        signature,
    ):
        #   signature: Signature,

        self.chunk_hash = chunk_hash
        self.prev_block_hash = prev_block_hash
        self.outcome_root = outcome_root
        self.encoded_merkle_root = encoded_merkle_root
        self.encoded_length = encoded_length
        self.height_created = height_created
        self.height_included = height_included
        self.shard_id = shard_id
        self.gas_used = gas_used
        self.gas_limit = gas_limit
        self.rent_paid = rent_paid
        self.validator_reward = validator_reward
        self.balance_burnt = balance_burnt
        self.outgoing_receipts_root = outgoing_receipts_root
        self.tx_root = tx_root
        self.validator_proposals = validator_proposals
        self.signature = signature


class StreamerMessage:
    def __init__(self, block, shards):
        self.block = block
        self.shards = shards


class BlockView:
    def __init__(self, author: str, header: BlockHeaderView, chunks: ChunkHeaderView):
        self.author = author
        self.header = header
        self.chunks = chunks
