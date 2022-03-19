import { ethers } from 'ethers';
import axios from 'axios';

export async function getNFTData(contract, nft) {
  const tokenURI = await contract.tokenURI(nft.tokenId);
  const { data: meta } = await axios.get(tokenURI);
  const price = ethers.utils.formatUnits(nft.price.toString(), 'ether');
  const item = {
    price,
    tokenId: nft.tokenId.toNumber(),
    seller: nft.seller,
    owner: nft.owner,
    name: meta.name,
    description: meta.description,
    image: meta.image,
    tokenURI,
  };
  return item;
}
