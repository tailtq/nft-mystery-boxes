import json
from pathlib import Path
from copy import deepcopy
import os
import requests

from brownie import network

from scripts.create_character import create_character, character_image
from scripts.deploy import get_nft_contract
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, PINATA_BASE_URL, get_account

metadata_template = {
    "name": "",
    "description": "",
    "image": "",
    "attributes": [
        {"trait_type": "Strength", "value": 0},
        {"trait_type": "Dexterity", "value": 0},
        {"trait_type": "Constitution", "value": 0},
        {"trait_type": "Intelligence", "value": 0},
        {"trait_type": "Wisdom", "value": 0},
        {"trait_type": "Charisma", "value": 0},
        {"trait_type": "Experience", "value": 0},
    ],
}


def create_metadata():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        create_character()

    account = get_account()
    tai_world = get_nft_contract()
    # tai_world.setBaseURI("https://gateway.pinata.cloud/ipfs/", {"from": account})

    token_id = tai_world.getNumberOfCharacters({"from": account}) - 1
    (
        name,
        strength,
        dexterity,
        constitution,
        intelligence,
        wisdom,
        charisma,
        _,
    ) = tai_world.characters(token_id)
    character = deepcopy(metadata_template)
    character["name"] = name
    character["description"] = "An NFT created in Tai World contract"
    character["image"] = "https://gateway.pinata.cloud/ipfs/" + upload_to_ipfs(
        character_image
    )
    character["attributes"][0]["value"] = dexterity
    character["attributes"][1]["value"] = strength
    character["attributes"][2]["value"] = constitution
    character["attributes"][3]["value"] = intelligence
    character["attributes"][4]["value"] = wisdom
    character["attributes"][5]["value"] = charisma

    dir_path = f"metadata/{network.show_active()}"
    json_path = f"{dir_path}/{name}-{token_id}.json"
    os.makedirs(dir_path, exist_ok=True)
    with open(json_path, "w") as f:
        f.write(json.dumps(character))
    cid = upload_to_ipfs(json_path)
    tx = tai_world.setCID(token_id, cid, {"from": account})
    tx.wait(1)

    print("Token URI:", tai_world.tokenURI(token_id))


def upload_to_ipfs(filepath: str):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = PINATA_BASE_URL + "/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": os.getenv("PINATA_API_KEY"),
            "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
        }
        response = requests.post(
            ipfs_url, files={"file": image_binary}, headers=headers
        )
        ipfs_hash = response.json()["IpfsHash"]
        return ipfs_hash
        # filename = filepath.split("/")[-1]
        # image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        # return image_uri


def main():
    create_metadata()
