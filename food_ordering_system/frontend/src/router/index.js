import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import UserLoginView from '@/views/UserLoginView.vue';
import UserDashboardView from "@/views/UserDashboardView.vue";
import ProfileView from '@/views/ProfileView.vue';
import OrderView from '@/views/OrderView.vue';
import OrderPlaceView from '@/views/OrderPlaceView.vue';
import MerchantDashboardView from "@/views/MerchantDashboardView.vue";
import MerchantSearchView from '@/views/MerchantSearchView.vue';
import MerchantDetailView from '@/views/MerchantDetailView.vue';
import MerchantLoginView from '@/views/MerchantLoginView.vue';
import DishSearchView from '@/views/DishSearchView.vue';
import DishDetailView from '@/views/DishDetailView.vue';

/* import RegisterView from '@/views/RegisterView.vue';
import MessagesView from '@/views/MessagesView.vue';
import AnalyticsView from '@/views/AnalyticsView.vue'; */

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/user_login', name: 'UserLogin', component: UserLoginView },
  { path: '/user_dashboard/:id', name: 'UserDashboardView', component: UserDashboardView},
  { path: '/profile', name: 'ProfileView', component: ProfileView },
  { path: '/order', name: 'Order', component: OrderView },
  { path: '/order/create', name: 'PlaceOrder', component: OrderPlaceView },
  { path: '/merchant_dashboard/:id', name: 'MerchantDashboardView', component: MerchantDashboardView},
  { path: '/merchant_login', name: 'MerchantLogin', component: MerchantLoginView },
  { path: '/merchants/search', name: 'MerchantSearch', component: MerchantSearchView },
  { path: '/merchants/:id', name: 'MerchantDetail', component: MerchantDetailView },
  { path: '/dishes/search/:id', name: 'DishSearch', component: DishSearchView },
  { path: '/dishes/:id', name: 'DishDetail', component: DishDetailView },

  /* { path: '/register', name: 'Register', component: RegisterView },
  { path: '/messages', name: 'Messages', component: MessagesView },
  { path: '/analytics', name: 'Analytics', component: AnalyticsView }, */
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
