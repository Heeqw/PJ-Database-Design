<template>
  <div>
    <UserLogoutButton />
    <h2>菜品搜索</h2>
    <input type="text" v-model="query" placeholder="输入菜品关键字">
    <button @click="searchDishes">搜索</button>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && dishes.length === 0">
      没有找到菜品。
    </div>

    <div v-if="dishes.length > 0">
      <h3>搜索结果:</h3>
      <ul>
        <li v-for="dish in dishes" :key="dish.id">
          <router-link :to="{ name: 'UserDishDetail', params: { id: dish.id } }">
          {{ dish.name }} - {{ dish.price }}
          <!--   还需要图片老师         -->
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: {UserLogoutButton},
  data() {
    return {
      query: '',
      loading: false,
      dishes: [],
      error: null,
      merchantId: null
    };
  },
  created() {
    // 可以在这里从路由参数中获取商家ID
    this.merchantId = this.$route.params.id;
    // 然后根据商家ID获取商家信息
    // 此处省略商家信息获取的代码，假设已经获取到了商家ID
    // this.merchantId = 4; // 假设商家ID为4
  },
  methods: {
    searchDishes() {
      this.loading = true;
      fetch(`http://127.0.0.1:8000/api/merchants/${this.merchantId}/dishes/search/?q=${this.query}`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.dishes = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = '搜索菜品失败';
            console.error('搜索菜品失败:', error);
          });
    }

  }
};
</script>

<style scoped>
/* 可以添加一些样式 */
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
}

li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>
