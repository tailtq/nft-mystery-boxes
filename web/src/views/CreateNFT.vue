<template>
  <div class="flex justify-center">
    <div class="w-1/2 flex flex-col pb-12">
      <input placeholder="Asset Name" class="mt-8 border rounded p-4" v-model="name" />
      <textarea
        placeholder="Asset Description"
        class="mt-2 border rounded p-4"
        v-model="description"
      />
      <input placeholder="Asset Price in Eth" class="mt-2 border rounded p-4" v-model="price" />
      <input type="file" name="Asset" className="my-4" @change="onChangeFile" />
      <img className="rounded mt-4" width="350" v-if="fileUrl" :src="fileUrl" />

      <button
        @click="listNFTForSale"
        class="font-bold mt-4 bg-pink-500 text-white rounded p-4 shadow-lg"
      >
        Create NFT
      </button>
    </div>
  </div>
</template>

<script>
import { ethers } from 'ethers';
import { create as ipfsHttpClient } from 'ipfs-http-client';
import Web3Modal from 'web3modal';
import { marketplaceAddress } from '../../config';

import NFTMarketplace from '../../artifacts/contracts/NFTMarketplace.sol/NFTMarketplace.json';

const client = ipfsHttpClient(process.env.VUE_APP_IPFS_SERVER);

export default {
  data() {
    return {
      name: '',
      description: '',
      price: '0',
      fileUrl: '',
    };
  },
  methods: {
    async onChangeFile(e) {
      const file = e.target.files[0];
      try {
        const added = await client.add(file, {
          progress: (prog) => console.log(`received: ${prog}`),
        });
        this.fileUrl = `https://ipfs.infura.io/ipfs/${added.path}`;
      } catch (error) {
        console.log('Error uploading file: ', error);
      }
    },
    async uploadFileToIPFS() {
      const { name, description, price, fileUrl } = this;
      if (!name || !description || !price || !fileUrl) return;
      const data = JSON.stringify({
        name,
        description,
        image: fileUrl,
      });
      try {
        const added = await client.add(data);
        const url = `https://ipfs.infura.io/ipfs/${added.path}`;
        return url;
      } catch (error) {
        console.log('Error uploading file: ', error);
      }
    },
    async listNFTForSale() {
      const url = await this.uploadFileToIPFS();
      const web3Modal = new Web3Modal();
      const connection = await web3Modal.connect();
      const provider = new ethers.providers.Web3Provider(connection);
      const signer = provider.getSigner();

      /* create the NFT */
      const price = ethers.utils.parseUnits(this.price, 'ether');
      const contract = new ethers.Contract(marketplaceAddress, NFTMarketplace.abi, signer);
      // console.log(contract, contract.getListingPrice());
      const listingPrice = (await contract.getListingPrice()).toString();
      const transaction = await contract.createToken(url, price, { value: listingPrice });
      await transaction.wait();

      this.$router.push('/');
    },
  },
};
</script>
