<template>
  <div>
    <h2>我的收藏</h2>
    <UserLogoutButton />
    <div v-if="loading">加载中...</div>

    <div v-if="favorites.length === 0 && !loading">
      <p>您还没有收藏任何商家。</p>
    </div>

    <div v-if="favorites.length > 0 && !loading">
      <h3>收藏的商家列表:</h3>
      <ul>
        <li v-for="favorite in favorites" :key="favorite.id">
          <router-link :to="{ name: 'MerchantDetail', params: { id: favorite.merchant } }">
            {{ favorite.merchantInfo ? favorite.merchantInfo.name : '加载中...' }}
            - {{ favorite.merchantInfo ? favorite.merchantInfo.address : '加载中...' }}
            - {{ favorite.merchantInfo ? favorite.merchantInfo.phone : '加载中...' }}
          </router-link>
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
      loading: true,
      favorites: [],
      error: null
    };
  },
  mounted() {
    this.fetchFavoriteMerchants();
    this.fetchMerchantInfo()
  },
  methods: {
    fetchMerchantInfo(merchantId) {
      axios.get(`http://127.0.0.1:8000/api/merchants/${merchantId}/`)
          .then(response => {
            // 处理返回的商家信息
            const merchantInfo = response.data;
            // 将商家信息添加到对应的收藏商家对象中
            const favoriteMerchant = this.favorites.find(favorite => favorite.merchant === merchantId);
            if (favoriteMerchant) {
              favoriteMerchant.merchantInfo = merchantInfo;
            }
          })
          .catch(error => {
            console.error('Error fetching merchant info:', error);
          });
    },
    fetchFavoriteMerchants() {
      axios.get('http://127.0.0.1:8000/api/users/favorites/merchants/')
          .then(response => {
            this.loading = false;
            this.favorites = response.data;
            // 遍历收藏的商家，获取商家详细信息
            this.favorites.forEach(favorite => {
              this.fetchMerchantInfo(favorite.merchant);
            });
          })
          .catch(error => {
            this.loading = false;
            this.error = '获取收藏商家失败';
            console.error('获取收藏商家失败:', error);
          });
    }

  }
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  margin: 0.5rem auto;
  padding: 0.5rem;
  width: 300px;
  border: 1px solid #ddd;
}

li a {
  text-decoration: none;
  color: inherit;
}
</style>
