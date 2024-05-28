<template>
  <div class="dish-details">
    <h1>{{ dish.name }}</h1>
    <div>
      <p><strong>Price:</strong> {{ dish.price }}</p>
      <p><strong>Category:</strong> {{ dish.category }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dish: {}
    };
  },
  created() {
    this.fetchDishData();
  },
  watch: {
    // 监听路由参数 id 的变化，当变化时重新获取菜品数据
    '$route.params.id': 'fetchDishData'
  },
  methods: {
    fetchDishData() {
      const dishId = this.$route.params.id;
      axios.get(`http://localhost:3000/api/dish_app_dish/${dishId}`)
          .then(response => {
            this.dish = response.data[0]; // 假设返回的数据只有一个菜品
          })
          .catch(error => {
            console.error('获取菜品数据时出错:', error);
          });
    }
  }
};
</script>

<style>

.details p {
  margin-bottom: 10px;
}
</style>
