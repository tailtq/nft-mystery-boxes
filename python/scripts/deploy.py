# from brownie import Contract, NFTMarketplace

# from scripts.utils import get_contract, get_account


# def deploy():
#     account = get_account()
#     print(account.balance())
#     active_network = network.show_active()

#     tai_world = TaiWorld.deploy(
#         get_contract("vrf_coordinator").address,
#         get_contract("link_token").address,
#         config["networks"][active_network]["vrf_key_hash"],
#         config["networks"][active_network]["vrf_gas_limit"],
#         get_contract("eth_usd_price_feed").address,
#         config["data"]["max_tokens"],
#         config["data"]["create_character_fee"],
#         "ipfs://",
#         {
#             "from": account,
#         },
#         publish_source=config["networks"][active_network].get("publish_source", False),
#     )
#     print(f"Contract has been deployed at {tai_world.address}!")
#     return tai_world


# def get_nft_contract():
#     if len(TaiWorld) == 0:
#         return deploy()
#     else:
#         return TaiWorld[-1]


def main():
    # print(123)
    pass
    # print(NFTMarketplace, "abc", NFTMarketplace._name)
    # contract = Contract.from_abi(
    #     NFTMarketplace._name,
    #     "0x5FbDB2315678afecb367f032d93F642f64180aa3",
    #     NFTMarketplace.abi,
    # )
