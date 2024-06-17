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
  { path: '/users/login', name: 'UserLogin', component: UserLoginView, meta: { breadcrumb:'用户登录' } },
  { path: '/users/dashboard/:id', name: 'UserDashboardView', component: UserDashboardView, meta: { breadcrumb:'用户仪表盘' } },
  { path: '/users/profile', name: 'UserProfileView', component: UserProfileView, meta: { breadcrumb:'用户资料' } },
  { path: '/users/order', name: 'UserOrder', component: UserOrderView, meta: { breadcrumb:'用户订单' } },
  { path: '/users/message', name: 'UserMessage', component: UserMessageView, meta: { breadcrumb:'消息列表' } },
  { path: '/users/order/detail/:id', name: 'UserOrderDetail', component: UserOrderDetailView, meta: { breadcrumb:'订单详情' } },
  { path: '/users/order/place/:id', name: 'OrderPlace', component: OrderPlaceView, meta: { breadcrumb:'下单' } },
  { path: '/users/favorites', name: 'UserFavorites', component: UserFavoritesView, meta: { breadcrumb:'收藏内容' } },
  { path: '/users/favorites/merchant', name: 'FavoriteMerchants', component: FavoriteMerchantView, meta: { breadcrumb:'收藏商家' } },
  { path: '/users/favorites/dish', name: 'FavoriteDishes', component: FavoriteDishView, meta: { breadcrumb:'收藏菜品' } },
  { path: '/merchants/dashboard/:id', name: 'MerchantDashboardView', component: MerchantDashboardView, meta: { breadcrumb:'商家仪表盘' } },
  { path: '/merchants/login', name: 'MerchantLogin', component: MerchantLoginView, meta: { breadcrumb:'商家登录' } },
  { path: '/users/merchants/search', name: 'MerchantSearch', component: MerchantSearchView, meta: { breadcrumb:'商家搜索' } },
  { path: '/users/merchants/:id', name: 'MerchantDetail', component: MerchantDetailView, meta: { breadcrumb:'商家详情' } },
  { path: '/merchants/profile/:id', name: 'MerchantProfile', component: MerchantProfileView, meta: { breadcrumb:'商家资料' } },
  { path: '/merchants/order', name: 'MerchantOrder', component: MerchantOrderView, meta: { breadcrumb:'商家订单' } },
  { path: '/merchants/order/detail/:id', name: 'MerchantOrderDetail', component: MerchantOrderDetailView, meta: { breadcrumb:'商家订单详情' } },
  { path: '/users/dishes/search/:id', name: 'DishSearch', component: DishSearchView, meta: { breadcrumb:'菜品搜索' } },
  { path: '/users/dishes/:id', name: 'UserDishDetail', component: UserDishDetailView, meta: { breadcrumb:'用户菜品详情' } },
  { path: '/merchants/dishes/:id', name: 'MerchantDishDetail', component: MerchantDishDetailView, meta: { breadcrumb:'商家菜品详情' } }
];



const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
