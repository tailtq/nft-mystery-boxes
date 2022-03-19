<template>
  <div class="flex justify-center">
    <div class="w-1/2 flex flex-col pb-12">
      <input placeholder="Asset Price in Eth" className="mt-2 border rounded p-4" v-model="price" />

      <img v-if="image" class="rounded mt-4" width="350" :src="image" />

      <button
        @click="listNFTForSale"
        class="font-bold mt-4 bg-pink-500 text-white rounded p-4 shadow-lg"
      >
        List NFT
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ethers } from 'ethers';
import Web3Modal from 'web3modal';

import { marketplaceAddress } from '../../config';
import NFTMarketplace from '../../artifacts/contracts/NFTMarketplace.sol/NFTMarketplace.json';

export default {
  data() {
    return {
      image: '',
      price: '0',
      tokenURI: '',
      id: '',
    };
  },
  async mounted() {
    const { id, tokenURI } = this.$route.query;
    this.id = id;
    this.tokenURI = tokenURI;
    await this.fetchNFT();
  },
  methods: {
    async fetchNFT() {
      const { tokenURI } = this.$route.query;
      if (!tokenURI) return;
      const { data: meta } = await axios.get(tokenURI);
      this.image = meta.image;
    },
    async listNFTForSale() {
      if (!this.price) return;
      const web3Modal = new Web3Modal();
      const connection = await web3Modal.connect();
      const provider = new ethers.providers.Web3Provider(connection);
      const signer = provider.getSigner();

      const priceFormatted = ethers.utils.parseUnits(this.price, 'ether');
      console.log(this.price, priceFormatted);
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, signer);
      const listingPrice = (await contract.getListingPrice()).toString();
      const transaction = await contract.resellToken(this.id, priceFormatted, {
        value: listingPrice,
      });
      await transaction.wait();
      this.$router.push('/');
    },
  },
};
</script>

<style></style>
