import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import UserLoginView from '@/views/UserLoginView.vue';
import UserDashboardView from "@/views/UserDashboardView.vue";
import UserProfileView from '@/views/UserProfileView.vue';
import UserOrderView from '@/views/UserOrderView.vue';
import UserMessageView from '@/views/UserMessageView.vue';
import OrderPlaceView from '@/views/OrderPlaceView.vue';
import MerchantDashboardView from "@/views/MerchantDashboardView.vue";
import MerchantSearchView from '@/views/MerchantSearchView.vue';
import MerchantDetailView from '@/views/MerchantDetailView.vue';
import MerchantProfileView from '@/views/MerchantProfileView.vue';
import MerchantLoginView from '@/views/MerchantLoginView.vue';
import MerchantOrderView from '@/views/MerchantOrderView.vue';
import DishSearchView from '@/views/DishSearchView.vue';
import DishDetailView from '@/views/DishDetailView.vue';

/* import RegisterView from '@/views/RegisterView.vue';
import AnalyticsView from '@/views/AnalyticsView.vue'; */

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/user_login', name: 'UserLogin', component: UserLoginView },
  { path: '/user_dashboard/:id', name: 'UserDashboardView', component: UserDashboardView},
  { path: '/profile', name: 'UserProfileView', component: UserProfileView },
  { path: '/user_order', name: 'UserOrder', component: UserOrderView },
  { path: '/user_message', name: 'UserMessage', component: UserMessageView },
  { path: '/order/place/:id', name: 'OrderPlace', component: OrderPlaceView },
  { path: '/merchant_dashboard/:id', name: 'MerchantDashboardView', component: MerchantDashboardView},
  { path: '/merchant_login', name: 'MerchantLogin', component: MerchantLoginView },
  { path: '/merchants/search', name: 'MerchantSearch', component: MerchantSearchView },
  { path: '/merchants/:id', name: 'MerchantDetail', component: MerchantDetailView },
  { path: '/merchants_profile/:id', name: 'MerchantProfile', component: MerchantProfileView },
  { path: '/merchant_order', name: 'MerchantOrder', component: MerchantOrderView },
  { path: '/dishes/search/:id', name: 'DishSearch', component: DishSearchView },
  { path: '/dishes/:id', name: 'DishDetail', component: DishDetailView },

  /* { path: '/register', name: 'Register', component: RegisterView },
    { path: '/analytics', name: 'Analytics', component: AnalyticsView }, */
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
