from brownie import TaiWorld, network
import pytest
from scripts.deploy import deploy

from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account


def skip_if_not_local_network():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()


def test_can_deploy_nft_success():
    skip_if_not_local_network()

    contract = deploy()

    assert contract is not None


# ===== Character
def test_can_create_character():
    skip_if_not_local_network()

    character_name = "Test Character"
    account = get_account()
    contract = deploy()
    fee = contract.getCreateCharacterFee({"from": account})

    funding_tx = fund_with_link(contract.address)
    funding_tx.wait(1)
    tx = contract.createCharacter(
        character_name, {"from": account, "value": fee + 1000000}
    )
    tx.wait(1)

    character_name_in_contract = contract.requestIdToName(
        tx.events["RequestedCharacter"]["requestId"]
    )
    assert character_name_in_contract == character_name


def test_cant_create_character_with_little_entrance_fee():
    skip_if_not_local_network()

    character_name = "Test Character"
    account = get_account()
    contract = deploy()
    fee = contract.getCreateCharacterFee({"from": account})

    # funding_tx = fund_with_link(contract.address)
    # funding_tx.wait(1)
    tx = contract.createCharacter(
        character_name, {"from": account, "value": fee - 1000000}
    )
    tx.wait(1)
    pass


def test_cant_create_character_without_link():
    pass


def test_cant_create_character_due_to_limit():
    pass


# ===== Metadata
def test_can_create_metadata():
    pass


def test_cant_create_metadata_without_contract_owner_permission():
    pass


def test_cant_create_metadata_without_character():
    pass


def test_can_withdraw_money_from_contract():
    pass


def test_cant_withdraw_moeny_from_contract_without_contract_owner_permission():
    pass
