import { createStore } from 'vuex';

export default createStore({
  state: {
    NFTs: [],
  },
  getters: {
  },
  mutations: {
    setNFTs(state, NFTs) {
      state.NFTs = NFTs;
    },
  },
  actions: {
    setNFTs({ commit }, NFTs) {
      commit('setNFTs', NFTs);
    },
  },
  modules: {
  },
});
