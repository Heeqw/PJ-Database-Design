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
        <li v-for=" merchant in paginatedAllMerchants" :key="merchant.id">
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
      <div>
        <button @click="changePageAllMerchants(-1)" :disabled="currentPageAllMerchants === 1">上一页</button>
        <button @click="changePageAllMerchants(1)" :disabled="currentPageAllMerchants === totalPagesAllMerchants">下一页</button>
      </div>
    </div>

    <div v-if="merchants.length > 0">
      <h3>搜索结果:</h3>
      <ul>
        <li v-for=" merchant in paginatedMerchants" :key="merchant.id">
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
      <div>
        <button @click="changePageMerchants(-1)" :disabled="currentPageMerchants === 1">上一页</button>
        <button @click="changePageMerchants(1)" :disabled="currentPageMerchants === totalPagesMerchants">下一页</button>
      </div>
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
      allMerchants: [], // 所有商家信息
      favoriteMerchants: [], // 已收藏的商家
      error: null,
      currentPageMerchants: 1, // 当前搜索结果页数
      pageSizeMerchants: 3, // 每页显示搜索结果数
      currentPageAllMerchants: 1, // 当前全部商家信息页数
      pageSizeAllMerchants: 3 // 每页显示全部商家信息数
    };
  },
  mounted() {
    this.fetchAllMerchants(); // 加载所有商家信息
    this.fetchFavoriteMerchants(); // 加载已收藏的商家
  },
  methods: {
    fetchAllMerchants() {
      axios.get('http://127.0.0.1:8000/api/merchants/search/')
          .then(response => {
            this.allMerchants = response.data;
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
      axios.get(`http://127.0.0.1:8000/api/merchants/search/?q=${this.query}`)
          .then(response => {
            this.loading = false;
            this.merchants = response.data;
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
            console.log('商家已收藏', response.data);
            alert('商家已收藏');
            this.favoriteMerchants.push(merchantId);
          })
          .catch(error => {
            console.error('添加收藏商家失败:', error);
            alert('添加收藏商家失败');
          });
    },
    isFavorite(merchantId) {
      return this.favoriteMerchants.includes(merchantId);
    },
    changePageMerchants(pageOffset) {
      this.currentPageMerchants += pageOffset;
    },
    changePageAllMerchants(pageOffset) {
      this.currentPageAllMerchants += pageOffset;
    }
  },
  computed: {
    paginatedMerchants() {
      const startIndex = (this.currentPageMerchants - 1) * this.pageSizeMerchants;
      return this.merchants.slice(startIndex, startIndex + this.pageSizeMerchants);
    },
    paginatedAllMerchants() {
      const startIndex = (this.currentPageAllMerchants - 1) * this.pageSizeAllMerchants;
      return this.allMerchants.slice(startIndex, startIndex + this.pageSizeAllMerchants);
    },
    totalPagesMerchants() {
      return Math.ceil(this.merchants.length / this.pageSizeMerchants);
    },
    totalPagesAllMerchants() {
      return Math.ceil(this.allMerchants.length / this.pageSizeAllMerchants);
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
