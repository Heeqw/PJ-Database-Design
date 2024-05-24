import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import ProfileView from '@/views/ProfileView.vue';
import MerchantSearchView from '@/views/MerchantSearchView.vue';
import MerchantDetailView from '@/views/MerchantDetailView.vue';
import DishSearchView from '@/views/DishSearchView.vue';
import DishDetailView from '@/views/DishDetailView.vue';
import OrderView from '@/views/OrderView.vue';
import MessagesView from '@/views/MessagesView.vue';
import AnalyticsView from '@/views/AnalyticsView.vue';

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },
  { path: '/profile', name: 'Profile', component: ProfileView },
  { path: '/merchants', name: 'MerchantSearch', component: MerchantSearchView },
  { path: '/merchants/:id', name: 'MerchantDetail', component: MerchantDetailView },
  { path: '/dishes', name: 'DishSearch', component: DishSearchView },
  { path: '/dishes/:id', name: 'DishDetail', component: DishDetailView },
  { path: '/order', name: 'Order', component: OrderView },
  { path: '/messages', name: 'Messages', component: MessagesView },
  { path: '/analytics', name: 'Analytics', component: AnalyticsView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;