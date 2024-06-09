<template>
  <div>
    <MerchantLogoutButton />
    <h1>商家详情</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <p>名称：{{ merchant.name }}</p>
      <p>地址：{{ merchant.address }}</p>
      <p>电话：{{ merchant.phone }}</p>

      <!-- 商家详细信息 -->

      <h2>菜品列表</h2>
      <div v-if="loadingDishes">加载菜品中...</div>
      <div v-else-if="dishes.length === 0">暂无菜品。</div>
      <div v-else>
        <ul>
          <li v-for="dish in dishes" :key="dish.id">
            <router-link :to="{ name: 'MerchantDishDetail', params: { id: dish.id } }">
              <p>名称：{{ dish.name }}</p>
              <p>编号：{{ dish.id }}</p>
              <p>价格：{{ dish.price }}</p>
              <p>类别：{{ dish.category }}</p>
            </router-link>
            <el-button type=danger @click="deleteDish(dish.id)">删除</el-button>
            <el-button type=success @click="setFeaturedDish(dish.id)">设置为主打菜</el-button> <!-- 新添加的按钮 -->
          </li>
        </ul>
      </div>
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
    // 获取商家详情
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
            this.error = '获取商家详情失败';
            console.error('获取商家详情失败:', error);
          });
    },
    // 获取商家菜品列表
    fetchMerchantDishes() {
      const merchantId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/merchants/${merchantId}/dishes/search/`)
          .then(response => response.json())
          .then(data => {
            this.loadingDishes = false;
            this.dishes = data;
          })
          .catch(error => {
            this.loadingDishes = false;
            this.errorDishes = '获取菜品失败';
            console.error('获取菜品失败:', error);
          });
    },
    // 删除菜品
    deleteDish(dishId) {
      const token = localStorage.getItem('token'); // 假设 token 存储在本地存储中
      fetch(`http://127.0.0.1:8000/api/merchants/delete_dish/${dishId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            if (response.ok) {
              // 从列表中移除被删除的菜品
              this.dishes = this.dishes.filter(dish => dish.id !== dishId);
              alert('菜品删除成功');
            } else {
              throw new Error('删除菜品失败！');
            }
          })
          .catch(error => {
            console.error('删除菜品失败:', error);
            alert('删除菜品失败');
          });
    },
    // 设置主打菜品
    setFeaturedDish(dishId) {
      const token = localStorage.getItem('token'); // 假设 token 存储在本地存储中
      fetch(`http://127.0.0.1:8000/api/merchants/set_featured_dish/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          dish_id: dishId
        })
      })
          .then(response => {
            if (response.ok) {
              alert('主打菜品设置成功');
              // 刷新菜品列表
              this.fetchMerchantDishes();
            } else {
              throw new Error('设置主打菜品失败！');
            }
          })
          .catch(error => {
            console.error('设置主打菜品失败:', error);
            alert('设置主打菜品失败');
          });
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

