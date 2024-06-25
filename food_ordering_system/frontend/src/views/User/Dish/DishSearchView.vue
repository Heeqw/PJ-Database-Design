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
        <li v-for="dish in paginatedDishes" :key="dish.id">
          <router-link :to="{ name: 'UserDishDetail', params: { id: dish.id } }">
            <div class="dish-info">
              <img :src="dish.image_url" alt="菜品图片" class="dish-image">
              <div class="dish-details">
                <p>{{ dish.name }}</p>
                <p>{{ dish.price }}</p>
              </div>
            </div>
          </router-link>
        </li>
      </ul>
      <div>
        <button @click="changePage(-1)" :disabled="currentPage === 1">上一页</button>
        <button @click="changePage(1)" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      query: "",
      loading: false,
      dishes: [],
      error: null,
      merchantId: null,
      currentPage: 1,
      pageSize: 3 // 每页显示的菜品数量
    };
  },
  created() {
    // 从路由参数中获取商家ID
    this.merchantId = this.$route.params.id;
    // 根据商家ID获取商家信息，如果需要可以在这里加载商家信息
  },
  methods: {
    searchDishes() {
      this.loading = true;
      fetch(`http://127.0.0.1:8000/api/merchants/${this.merchantId}/dishes/search/?q=${this.query}`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.dishes = data;
            this.currentPage = 1; // 搜索后将当前页数重置为第一页
          })
          .catch(error => {
            this.loading = false;
            this.error = "搜索菜品失败";
            console.error("搜索菜品失败:", error);
          });
    },
    changePage(pageOffset) {
      this.currentPage += pageOffset;
    }
  },
  computed: {
    paginatedDishes() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      return this.dishes.slice(startIndex, startIndex + this.pageSize);
    },
    totalPages() {
      return Math.ceil(this.dishes.length / this.pageSize);
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
}

li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}

.dish-info {
  display: flex;
  align-items: center;
}

.dish-image {
  width: 100px; /* 调整图片宽度 */
  height: auto;
  margin-right: 10px;
}

.dish-details {
  flex: 1;
}
</style>
