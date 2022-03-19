from web3 import Web3
from brownie import network

from scripts.deploy import get_nft_contract
from scripts.utils import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    fund_with_link,
    get_account,
    get_contract,
)

character_name = "Uchiha Itachi"
character_image = "metadata/itachi.jpeg"


def create_character():
    account = get_account()
    tai_world = get_nft_contract()

    funding_tx = fund_with_link(tai_world.address, amount=Web3.toWei(0.1, "ether"))
    funding_tx.wait(1)
    print("Fund link token successfully.")

    fee = tai_world.getCreateCharacterFee({"from": account})
    tx = tai_world.createCharacter(
        character_name, {"from": account, "value": fee + 1000000}
    )
    tx.wait(1)

    request_id = tx.events["RequestedCharacter"]["requestId"]
    print("A new character has been requested.\n")

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        STATIC_RNG = 12314555
        randomness_tx = get_contract("vrf_coordinator").callBackWithRandomness(
            request_id, STATIC_RNG, tai_world.address, {"from": account}
        )
        randomness_tx.wait(1)
        print(
            f"A new character has been created. Its stats are: {tai_world.characters(0)}.\n"
        )


def main():
    create_character()
