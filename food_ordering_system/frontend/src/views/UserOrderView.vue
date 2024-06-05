<template>
  <div>
    <UserLogoutButton />
    <h2>订单总览</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && orders.length === 0">
      没有订单记录。
    </div>

    <div v-if="orders.length > 0">
      <h3>订单列表:</h3>
      <ul>
        <li v-for="order in orders" :key="order.id">
          <p>订单时间: {{ order.date }}</p>
          <p>状态: {{ order.status }}</p>
          <p>类型: {{ order.type }}</p>
          <p>总价: {{ order.total_price }}</p>
          <p>商家: {{ order.merchant }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: {UserLogoutButton},
  data() {
    return {
      orders: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchOrderHistory();

  },
  methods: {
    fetchOrderHistory() {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      console.log('Token:', token);
      axios.get('http://127.0.0.1:8000/api/orders/order_history')
          .then(response => {
            console.log('Response data:', response.data); // 调试：打印响应数据
            this.orders = response.data;
            this.loading = false;
          })
          .catch(error => {
            console.error('获取订单历史失败:', error);
            this.error = '获取订单历史失败';
            this.loading = false;
          });
    }
  }
};
</script>

<style scoped>
/* 添加一些样式使页面更好看 */
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

p {
  margin: 0.2rem 0;
}
</style>
