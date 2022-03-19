import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import CreateNFT from '../views/CreateNFT.vue';
import MyNFTs from '../views/MyNFTs.vue';
import CreatorDashboard from '../views/CreatorDashboard.vue';
import ResellNFT from '../views/ResellNFT.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/create-nft',
    name: 'create-nft',
    component: CreateNFT,
  },
  {
    path: '/my-nfts',
    name: 'my-nfts',
    component: MyNFTs,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: CreatorDashboard,
  },
  {
    path: '/resell-nft',
    name: 'resell-nft',
    component: ResellNFT,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
