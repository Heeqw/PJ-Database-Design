<template>
  <div>
    <UserLogoutButton />
    <el-button type="primary" @click="goToDishSearch">搜索菜品</el-button>
    <el-button type="primary" @click="goToOrderPlace">我要下单</el-button>
    <el-button type="primary" @click="viewLoyal">忠实顾客</el-button>
    <el-button type="primary" @click="viewTrend">销售趋势查看</el-button>
    <h1>商家详细信息</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>名称：{{ merchant.name }}</p>
      <p>地址：{{ merchant.address }}</p>
      <p>手机：{{ merchant.phone }}</p>

      <h2>菜品</h2>
      <div v-if="loadingDishes">Loading dishes...</div>
      <div v-else-if="dishes.length === 0">No dishes found.</div>
      <div v-else>
        <ul>
          <li v-for="dish in dishes" :key="dish.id">
            <router-link :to="{ name: 'UserDishDetail', params: { id: dish.id } }">
              <p>名称：{{ dish.name }}</p>
              <p>Id: {{ dish.id }}</p>
              <p>价格：{{ dish.price }}</p>
            <p>收藏量: {{ dish.favorite_count }}</p>
            <p>线上销量: {{ dish.online_sales }}</p>
            <p>线下销量: {{ dish.offline_sales }}</p>
            <p>评分: {{ dish.avg_rating }}</p>
            <p>总订单数: {{ dish.total_orders }}</p>
            <p>最高订单用户: {{ dish.top_customer?.username }}</p>
            </router-link>
            <span v-if="isDishFavorite(dish.id)" class="favorite-star">⭐</span>

            <el-button
                type="success"
                @click="addFavorite(dish.id)"
                :disabled="isDishFavorite(dish.id)"
            >
              收藏
            </el-button>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";
import axios from 'axios';

export default {
  components: { UserLogoutButton },
  data() {
    return {
      loading: true,
      loadingDishes: true,
      merchant: null,
      dishes: [],
      favoriteDishes: [], // 存储已收藏的菜品
      error: null,
      errorDishes: null
    };
  },
  mounted() {
    this.fetchMerchantDetails();
    this.fetchMerchantDishes();
    this.fetchFavoriteDishes(); // 加载已收藏的菜品
  },
  methods: {
    fetchMerchantDetails() {
      const merchantId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/api/merchants/${merchantId}/`)
          .then(response => {
            this.loading = false;
            this.merchant = response.data;
          })
          .catch(error => {
            this.loading = false;
            this.error = 'Failed to fetch merchant details';
            console.error('Error fetching merchant details:', error);
          });
    },
    fetchMerchantDishes() {
      const merchantId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/api/merchants/${merchantId}/dishes/search/`)
          .then(response => {
            this.loadingDishes = false;
            this.dishes = response.data;
            this.fetchDishFavoritesCount();
            this.fetchDishSalesCount();
            this.fetchDishStatistics();
          })
          .catch(error => {
            this.loadingDishes = false;
            this.errorDishes = 'Failed to fetch dishes';
            console.error('Error fetching dishes:', error);
          });
    },
    fetchDishFavoritesCount() {
      const merchantId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/api/dishes/dish_favorites_count/${merchantId}/`)
          .then(response => {
            this.dishes.forEach(dish => {
              const favData = response.data.find(item => item.dish_id === dish.id);
              dish.favorite_count = favData ? favData.favorites_count : 0;
            });
          })
          .catch(error => {
            console.error('Error fetching dish favorites count:', error);
          });
    },
    fetchDishSalesCount() {
      const merchantId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/api/dishes/dish_sales_count/${merchantId}/`)
          .then(response => {
            this.dishes.forEach(dish => {
              const salesData = response.data.find(item => item.dish_id === dish.id);
              dish.online_sales = salesData ? salesData.online_sales : 0;
              dish.offline_sales = salesData ? salesData.offline_sales : 0;
            });
          })
          .catch(error => {
            console.error('Error fetching dish sales count:', error);
          });
    },
    fetchDishStatistics() {
      const merchantId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/api/analytics/dish_statistics/${merchantId}/`)
          .then(response => {
            this.dishes.forEach(dish => {
              const statsData = response.data.find(item => item.dish.id === dish.id);
              if (statsData) {
                dish.avg_rating = statsData.avg_rating;
                dish.total_orders = statsData.total_orders;
                dish.top_customer = statsData.top_customer;
              }
            });
          })
          .catch(error => {
            console.error('Error fetching dish statistics:', error);
          });
    },
    fetchFavoriteDishes() {
      axios.get('http://127.0.0.1:8000/api/users/favorites/dishes/')
          .then(response => {
            this.favoriteDishes = response.data.map(fav => fav.dish);
          })
          .catch(error => {
            console.error('获取收藏菜品信息失败:', error);
          });
    },
    addFavorite(dishId) {
      axios.post('http://127.0.0.1:8000/api/users/add_favorite_dish/', { dish_id: dishId })
          .then(response => {
            console.log('Response data:', response.data);
            alert('成功收藏菜品！');
            // 更新已收藏的菜品列表
            this.favoriteDishes.push(dishId);
            // 更新收藏量
            const dish = this.dishes.find(dish => dish.id === dishId);
            if (dish) {
              dish.favorite_count += 1;
            }
          })
          .catch(error => {
            console.error('Error adding favorite dish:', error);
            alert('Failed to add favorite dish');
          });
    },
    isDishFavorite(dishId) {
      return this.favoriteDishes.includes(dishId);
    },
    goToDishSearch() {
      const merchantId = this.$route.params.id;
      this.$router.push({ name: 'DishSearch', params: { id: merchantId } });
    },
    goToOrderPlace() {
      const merchantId = this.$route.params.id;
      this.$router.push({ name: 'OrderPlace', params: { id: merchantId } });
    },
    viewLoyal() {
      const merchantId = this.$route.params.id;
      this.$router.push({ name: 'UserMerchantLoyalCustomers', params: { id: merchantId } });
    },
    viewTrend() {
      const merchantId = this.$route.params.id;
      this.$router.push({ name: 'UserMerchantTrends', params: { id: merchantId } });
    },
  }
};
</script>

<style scoped>
.details p {
  margin-bottom: 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  background: #f9f9f9;
  width: 400px;
  margin: 0.5rem auto;
  padding: 10px;
  border: 1px solid #ddd;
  position: relative; /* 添加相对定位 */
}
li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>

