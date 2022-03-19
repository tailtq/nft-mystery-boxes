<template>
  <EmptyItemsMessage
    v-if="loaded && NFTs.length === 0"
    :message="'No items available'"
  ></EmptyItemsMessage>
  <div v-else class="flex justify-center">
    <div class="px-4" style="max-width: 1600px">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-4">
        <NFTCard
          v-for="(nft, i) in NFTs"
          :key="i"
          :nft="nft"
          :btn-text="'Buy'"
          :btn-action="buyNFT"
          :render-title-and-description="true"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ethers } from 'ethers';
import Web3Modal from 'web3modal';

import { marketplaceAddress } from '../../config';
import NFTMarketplace from '../../artifacts/contracts/NFTMarketplace.sol/NFTMarketplace.json';
import EmptyItemsMessage from '@/components/EmptyItemsMessage.vue';
import NFTCard from '@/components/NFTCard.vue';
import { getNFTData } from '@/utils/NFTUtils';

export default {
  components: {
    EmptyItemsMessage,
    NFTCard,
  },
  data() {
    return {
      loaded: false,
    };
  },
  computed: {
    NFTs() {
      return this.$store.state.NFTs;
    },
  },
  methods: {
    async loadNFTs() {
      const provider = new ethers.providers.JsonRpcProvider();
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, provider);
      const data = await contract.fetchMarketItems();

      const items = await Promise.all(data.map(async (nft) => getNFTData(contract, nft)));
      this.$store.dispatch('setNFTs', items);
      this.loaded = true;
    },
    async buyNFT(nft) {
      const web3Modal = new Web3Modal();
      const connection = await web3Modal.connect();
      const provider = new ethers.providers.Web3Provider(connection);
      const signer = provider.getSigner();
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, signer);

      /* user will be prompted to pay the asking proces to complete the transaction */
      const price = ethers.utils.parseUnits(nft.price.toString(), 'ether');
      const transaction = await contract.createMarketSale(nft.tokenId, { value: price });
      await transaction.wait();
      await this.loadNFTs();
    },
  },
  mounted() {
    this.loadNFTs();
  },
};
</script>
