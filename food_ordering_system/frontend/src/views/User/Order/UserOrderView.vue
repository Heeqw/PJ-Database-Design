<template>
  <div>
    <UserLogoutButton />
    <h2>订单总览</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="error">{{ error }}</div>

    <div v-if="!loading && orders.length === 0">
      没有订单记录。
    </div>

    <div v-if="orders.length > 0">
      <h3>订单列表:</h3>
      <ul>
        <li v-for=" order in paginatedOrders" :key="order.id" class="order-item">
          <router-link :to="{ name: 'UserOrderDetail', params: { id: order.id } }" class="order-link">
            <div>
              <p>订单id: {{ order.id }}</p>
              <p>订单时间: {{ order.date }}</p>
              <p>状态: {{ order.status }}</p>
              <p>类型: {{ order.type }}</p>
              <p>总价: {{ order.total_price }}</p>
              <p>商家: {{ order.merchant }}</p>
            </div>
          </router-link>
        </li>
      </ul>
      <div>
        <p>共 {{ orders.length }} 条订单</p>
        <p>当前页 {{ currentPage }} / {{ totalPages }}</p>
        <button @click="changePage(-1)" :disabled="currentPage === 1">上一页</button>
        <button @click="changePage(1)" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      orders: [],
      loading: true,
      error: null,
      currentPage: 1,
      pageSize: 3
    };
  },
  created() {
    this.fetchOrderHistory();
  },
  methods: {
    fetchOrderHistory() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:8000/api/orders/order_history', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            this.orders = response.data;
            this.loading = false;
          })
          .catch(error => {
            console.error('获取订单历史失败:', error);
            this.error = '获取订单历史失败';
            this.loading = false;
          });
    },
    changePage(pageOffset) {
      this.currentPage += pageOffset;
    }
  },
  computed: {
    paginatedOrders() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      return this.orders.slice(startIndex, startIndex + this.pageSize);
    },
    totalPages() {
      return Math.ceil(this.orders.length / this.pageSize);
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
  width: 400px;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
}

.order-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.order-item p {
  margin: 0.2rem 0;
}
</style>
