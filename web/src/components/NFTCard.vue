<template>
  <div class="border shadow rounded-xl overflow-hidden">
    <img :src="nft.image" />
    <div v-if="renderTitleAndDescription" class="p-4">
      <p style="height: 64px" class="text-2xl font-semibold">{{ nft.name }}</p>
      <div style="height: 70px; overflow: hidden">
        <p class="text-gray-400">{{ nft.description }}</p>
      </div>
    </div>
    <div class="p-4 bg-black">
      <p class="text-2xl font-bold text-white">{{ nft.price }} ETH</p>
      <button
        v-if="btnAction && btnText"
        class="mt-4 w-full bg-pink-500 text-white font-bold py-2 px-12 rounded"
        @click="btnAction(nft)"
      >
        {{ btnText }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    nft: {
      type: Object,
    },
    btnAction: {
      type: Function,
    },
    btnText: {
      type: String,
    },
    renderTitleAndDescription: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
