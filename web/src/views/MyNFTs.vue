<template>
  <EmptyItemsMessage
    v-if="loaded && nfts.length === 0"
    :message="'No items available'"
  ></EmptyItemsMessage>

  <div v-else class="flex justify-content">
    <div class="p-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <NFTCard
          v-for="(nft, i) in nfts"
          :key="i"
          :nft="nft"
          :btn-text="'List'"
          :btn-action="listNFT"
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
      nfts: [],
      loaded: false,
    };
  },
  async mounted() {
    await this.loadMyNFTs();
  },
  methods: {
    async loadMyNFTs() {
      // const provider = new ethers.providers.JsonRpcProvider();
      const web3Modal = new Web3Modal();
      const connection = await web3Modal.connect();
      const provider = new ethers.providers.Web3Provider(connection);
      const signer = provider.getSigner();
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, signer);
      const data = await contract.fetchMyNFTs();

      const items = await Promise.all(data.map(async (nft) => getNFTData(contract, nft)));
      this.nfts = items;
      this.loadingState = true;
    },
    listNFT(nft) {
      this.$router.push(`/resell-nft?id=${nft.tokenId}&tokenURI=${nft.tokenURI}`);
    },
  },
};
</script>
