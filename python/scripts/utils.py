from brownie import (
    network,
    accounts,
    config,
    TaiWorld,
    LinkToken,
    MockV3Aggregator,
    VRFCoordinatorMock,
    Contract,
)
from web3 import Web3

PINATA_BASE_URL = "https://api.pinata.cloud"
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "hardhat-test"]
CONTRACTS = {
    "nft": TaiWorld,
    "link_token": LinkToken,
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
}
ETH_IN_USD = 258900000000


def get_account(index: int = None, id: str = None):
    # accounts[0]
    # accounts.add("env")
    # accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_contract(name: str):
    """
    Get contract based on predefined name
    """
    if name not in CONTRACTS:
        return None

    network_name = network.show_active()
    contract_type = CONTRACTS[name]

    if network_name in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) == 0:
            # deploy all mocks
            _deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network_name][name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def _deploy_mocks():
    """
    Deploy mocks for local development
    """
    account = get_account()
    MockV3Aggregator.deploy(8, ETH_IN_USD, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})


def fund_with_link(
    contract_address: str, account=None, amount=Web3.toWei(0.1, "ether")
):
    """
    0.1 link will be funded to the specified contract address
    """
    account = account if account else get_account()
    link_token = get_contract("link_token")  # ???
    tx = link_token.transfer(contract_address, amount, {"from": account})
    return tx
