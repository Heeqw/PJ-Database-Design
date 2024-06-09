import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import UserLoginView from '@/views/User/UserLoginView.vue';
import UserDashboardView from "@/views/User/UserDashboardView.vue";
import UserProfileView from '@/views/User/UserProfileView.vue';
import UserOrderView from '@/views/User/Order/UserOrderView.vue';
import UserMessageView from '@/views/User/UserMessageView.vue';
import UserOrderDetailView from '@/views/User/Order/UserOrderDetailView.vue';
import UserFavoritesView from "@/views/User/UserFavoritesView.vue";
import OrderPlaceView from '@/views/User/Order/OrderPlaceView.vue';
import MerchantDashboardView from "@/views/Merchant/MerchantDashboardView.vue";
import MerchantSearchView from '@/views/User/Merchant/MerchantSearchView.vue';
import MerchantDetailView from '@/views/User/Merchant/MerchantDetailView.vue';
import MerchantProfileView from '@/views/Merchant/MerchantProfileView.vue';
import MerchantLoginView from '@/views/Merchant/MerchantLoginView.vue';
import MerchantOrderView from '@/views/Merchant/MerchantOrderView.vue';
import MerchantOrderDetailView from '@/views/Merchant/MerchantOrderDetailView.vue';
import DishSearchView from '@/views/User/Dish/DishSearchView.vue';
import UserDishDetailView from '@/views/User/Dish/UserDishDetailView.vue';
import MerchantDishDetailView from '@/views/Merchant/MerchantDishDetailView.vue';
import FavoriteMerchantView from "@/views/User/Merchant/FavoriteMerchantView.vue";
import FavoriteDishView from "@/views/User/Dish/FavoriteDishView.vue";

/* import RegisterView from '@/views/RegisterView.vue';
import AnalyticsView from '@/views/AnalyticsView.vue'; */

const routes = [
  { path: '/', name: 'Home', component: HomeView, meta: { title: '首页' } },
  { path: '/user_login', name: 'UserLogin', component: UserLoginView, meta: { title: '用户登录' } },
  { path: '/user_dashboard/:id', name: 'UserDashboardView', component: UserDashboardView, meta: { title: '用户仪表盘' } },
  { path: '/profile', name: 'UserProfileView', component: UserProfileView, meta: { title: '用户资料' } },
  { path: '/user_order', name: 'UserOrder', component: UserOrderView, meta: { title: '用户订单' } },
  { path: '/user_message', name: 'UserMessage', component: UserMessageView, meta: { title: '用户消息' } },
  { path: '/user_order/detail/:id', name: 'UserOrderDetail', component: UserOrderDetailView, meta: { title: '订单详情' } },
  { path: '/order/place/:id', name: 'OrderPlace', component: OrderPlaceView, meta: { title: '下单' } },
  { path: '/user/favorites', name: 'UserFavorites', component: UserFavoritesView, meta: { title: '收藏内容' } },
  { path: '/user/favorites/merchant', name: 'FavoriteMerchants', component: FavoriteMerchantView, meta: { title: '收藏商家' } },
  { path: '/user/favorites/dish', name: 'FavoriteDishes', component: FavoriteDishView, meta: { title: '收藏菜品' } },
  { path: '/merchant_dashboard/:id', name: 'MerchantDashboardView', component: MerchantDashboardView, meta: { title: '商家仪表盘' } },
  { path: '/merchant_login', name: 'MerchantLogin', component: MerchantLoginView, meta: { title: '商家登录' } },
  { path: '/merchants/search', name: 'MerchantSearch', component: MerchantSearchView, meta: { title: '商家搜索' } },
  { path: '/merchants/:id', name: 'MerchantDetail', component: MerchantDetailView, meta: { title: '商家详情' } },
  { path: '/merchants_profile/:id', name: 'MerchantProfile', component: MerchantProfileView, meta: { title: '商家资料' } },
  { path: '/merchant_order', name: 'MerchantOrder', component: MerchantOrderView, meta: { title: '商家订单' } },
  { path: '/merchant_order/detail/:id', name: 'MerchantOrderDetail', component: MerchantOrderDetailView, meta: { title: '商家订单详情' } },
  { path: '/dishes/search/:id', name: 'DishSearch', component: DishSearchView, meta: { title: '菜品搜索' } },
  { path: '/users/dishes/:id', name: 'UserDishDetail', component: UserDishDetailView, meta: { title: '用户菜品详情' } },
  { path: '/merchants/dishes/:id', name: 'MerchantDishDetail', component: MerchantDishDetailView, meta: { title: '商家菜品详情' } }
];



const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
