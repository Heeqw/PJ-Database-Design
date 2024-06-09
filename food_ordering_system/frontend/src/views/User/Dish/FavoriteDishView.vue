<template>
  <div>
    <h2>用户收藏的菜品</h2>
    <div v-if="loading">加载中...</div>

    <div v-if="!loading && favorites.length === 0">
      <p>您还没有收藏任何菜品。</p>
    </div>

    <div v-if="favorites.length > 0">
      <ul>
        <li v-for="favorite in favorites" :key="favorite.id">
          <div v-if="favorite.dishInfo">
            <router-link :to="{ name: 'UserDishDetail', params: { id: favorite.dishInfo.id } }">
              {{ favorite.dishInfo.name }} - {{ favorite.dishInfo.price }}
            </router-link>
          </div>
          <div v-else>
            <p>加载中...</p>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: true,
      favorites: []
    };
  },
  mounted() {
    this.fetchFavoriteDishes();
  },
  methods: {
    fetchFavoriteDishes() {
      axios.get('http://127.0.0.1:8000/api/users/favorites/dishes/')
          .then(response => {
            this.loading = false;
            this.favorites = response.data;
            this.fetchDishInfo();
          })
          .catch(error => {
            console.error('Error fetching favorite dishes:', error);
            this.loading = false;
          });
    },
    fetchDishInfo() {
      this.favorites.forEach(favorite => {
        axios.get(`http://127.0.0.1:8000/api/dishes/${favorite.dish}/`)
            .then(response => {
              favorite.dishInfo = response.data;
            })
            .catch(error => {
              console.error('Error fetching dish info:', error);
            });
      });
    }
  }
};
</script>

<style scoped>
/* 样式可以根据需要自行调整 */
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
