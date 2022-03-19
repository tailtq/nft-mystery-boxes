<template>
  <nav class="border-b p-6">
    <p class="text-4xl font-bold">Metaverse Marketplace</p>
    <div class="flex mt-4">
      <router-link to="/" class="mr-4 text-pink-500">Home</router-link>
      <router-link to="/create-nft" class="mr-6 text-pink-500">Sell NFT</router-link>
      <router-link to="/my-nfts" class="mr-6 text-pink-500">My NFTs</router-link>
      <router-link to="/dashboard" class="mr-6 text-pink-500">Dashboard</router-link>
    </div>
  </nav>

  <router-view />
</template>
