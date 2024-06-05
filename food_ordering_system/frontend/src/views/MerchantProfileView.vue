<template>
  <div>
    <MerchantLogoutButton />
    <h1>Merchant Details</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Name: {{ merchant.name }}</p>
      <p>Address: {{ merchant.address }}</p>
      <p>Phone: {{ merchant.phone }}</p>

      <!-- 商家详细信息 -->

      <h2>Dishes</h2>
      <div v-if="loadingDishes">Loading dishes...</div>
      <div v-else-if="dishes.length === 0">No dishes found.</div>
      <div v-else>
        <ul>
          <li v-for="dish in dishes" :key="dish.id">
            <router-link :to="{ name: 'DishDetail', params: { id: dish.id } }">
              <p>Name: {{ dish.name }}</p>
              <p>Id: {{ dish.id }}</p>
              <p>Price: {{ dish.price }}</p>
              <p>Category: {{ dish.category }}</p>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- 添加按钮跳转到搜索菜品页面 -->
      <el-button type="primary" class="dish-search-button" @click="goToDishSearch">搜索菜品</el-button>
      <el-button type="primary" class="order-place-button" @click="goToOrderPlace">我要下单</el-button>
    </div>
  </div>
</template>

<script>
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";

export default {
  components: {MerchantLogoutButton},
  data() {
    return {
      loading: true,
      loadingDishes: true,
      merchant: null,
      dishes: [],
      error: null,
      errorDishes: null
    };
  },
  mounted() {
    this.fetchMerchantDetails();
    this.fetchMerchantDishes();
  },
  methods: {
    fetchMerchantDetails() {
      const merchantId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/merchants/${merchantId}/`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.merchant = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = 'Failed to fetch merchant details';
            console.error('Error fetching merchant details:', error);
          });
    },
    fetchMerchantDishes() {
      const merchantId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/dishes/search/${merchantId}/`)
          .then(response => response.json())
          .then(data => {
            this.loadingDishes = false;
            this.dishes = data;
          })
          .catch(error => {
            this.loadingDishes = false;
            this.errorDishes = 'Failed to fetch dishes';
            console.error('Error fetching dishes:', error);
          });
    },
    goToDishSearch() {
      // 获取商家 ID
      const merchantId = this.$route.params.id;
      // 导航到搜索菜品页面，并传递商家 ID
      this.$router.push({ name: 'DishSearch', params: { id: merchantId } });
    },
    goToOrderPlace(){
      // 获取商家 ID
      const merchantId = this.$route.params.id;
      // 导航到点单页面，并传递商家 ID
      this.$router.push({ name: 'OrderPlace', params: { id: merchantId } });
    }

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
}
li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>
