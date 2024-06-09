<template>
  <div>
    <h2>商家搜索</h2>
    <UserLogoutButton />
    <input type="text" v-model="query" placeholder="输入搜索关键词">
    <el-button type="primary" class="search-merchant-button" @click="searchMerchants">搜索</el-button>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && merchants.length === 0">
      <p>没有搜索到商家。</p>
      <p v-if="allMerchants.length > 0">全部商家信息：</p>
      <ul>
        <li v-for="merchant in allMerchants" :key="merchant.id">
          <router-link :to="{ name: 'MerchantDetail', params: { id: merchant.id } }">
            {{ merchant.name }} - {{ merchant.address }} - {{ merchant.phone }}
            <p v-if="merchant.featured_dish">
              主打菜品: {{ merchant.featured_dish.name }} - ${{ merchant.featured_dish.price }}
            </p>
          </router-link>
          <span v-if="isFavorite(merchant.id)" class="favorite-star">⭐</span>
          <el-button
              type="success"
              @click="addFavoriteMerchant(merchant.id)"
              :disabled="isFavorite(merchant.id)"
          >
            收藏
          </el-button>
        </li>
      </ul>
    </div>

    <div v-if="merchants.length > 0">
      <h3>搜索结果:</h3>
      <ul>
        <li v-for="merchant in merchants" :key="merchant.id">
          <router-link :to="{ name: 'MerchantDetail', params: { id: merchant.id } }">
            {{ merchant.name }} - {{ merchant.address }} - {{ merchant.phone }}
            <p v-if="merchant.featured_dish">
              主打菜品: {{ merchant.featured_dish.name }} - ${{ merchant.featured_dish.price }}
            </p>
          </router-link>
          <span v-if="isFavorite(merchant.id)" class="favorite-star">⭐</span>
          <el-button
              type="success"
              @click="addFavoriteMerchant(merchant.id)"
              :disabled="isFavorite(merchant.id)"
          >
            收藏
          </el-button>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import UserLogoutButton from '@/components/UserLogoutButton.vue';
import axios from 'axios';

export default {
  components: {
    UserLogoutButton
  },
  data() {
    return {
      query: '',
      loading: false,
      merchants: [],
      allMerchants: [], // 添加一个新的数组来存储所有商家信息
      favoriteMerchants: [], // 存储已收藏的商家
      error: null
    };
  },
  mounted() {
    this.fetchAllMerchants(); // 加载所有商家信息
    this.fetchFavoriteMerchants(); // 加载已收藏的商家
  },
  methods: {
    fetchAllMerchants() {
      fetch(`http://127.0.0.1:8000/api/merchants/search/`)
          .then(response => response.json())
          .then(data => {
            this.allMerchants = data;
          })
          .catch(error => {
            console.error('获取全部商家信息失败:', error);
          });
    },
    fetchFavoriteMerchants() {
      axios.get('http://127.0.0.1:8000/api/users/favorites/merchants/')
          .then(response => {
            this.favoriteMerchants = response.data.map(fav => fav.merchant);
          })
          .catch(error => {
            console.error('获取收藏商家信息失败:', error);
          });
    },
    searchMerchants() {
      this.loading = true;
      fetch(`http://127.0.0.1:8000/api/merchants/search/?q=${this.query}`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.merchants = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = '获取搜索结果失败';
            console.error('获取搜索结果失败:', error);
          });
    },
    addFavoriteMerchant(merchantId) {
      axios.post('http://127.0.0.1:8000/api/users/add_favorite_merchant/', { merchant_id: merchantId })
          .then(response => {
            console.log('Response data:', response.data);
            alert('Merchant added to favorites');
            // 更新已收藏的商家列表
            this.favoriteMerchants.push(merchantId);
          })
          .catch(error => {
            console.error('Error adding favorite merchant:', error);
            alert('Failed to add favorite merchant');
          });
    },
    isFavorite(merchantId) {
      return this.favoriteMerchants.includes(merchantId);
    }
  }
};
</script>
<style scoped>
input {
  width: 200px;
  padding: 0.5rem;
  margin-right: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  width: 400px;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
  position: relative;
}

li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}

</style>
