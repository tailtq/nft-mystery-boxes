<template>
  <div className="p-4">
    <h2 className="text-2xl py-2">Items Listed</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <NFTCard v-for="(nft, i) in nfts" :key="i" :nft="nft" />
    </div>
  </div>
</template>

<script>
import { ethers } from 'ethers';

import { getNFTData } from '@/utils/NFTUtils';
import NFTCard from '@/components/NFTCard.vue';

export default {
  props: {
    NFTCard,
  },
  data() {
    return {
      nfts: [],
      loaded: false,
    };
  },
  methods: {
    async loadNFTs() {
      const provider = new ethers.providers.JsonRpcProvider();
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, provider);
      const data = await contract.fetchItemsListed();
      this.nfts = await Promise.all(data.map((nft) => getNFTData(contract, nft)));
      this.loaded = true;
    },
  },
};
</script>

<style></style>
