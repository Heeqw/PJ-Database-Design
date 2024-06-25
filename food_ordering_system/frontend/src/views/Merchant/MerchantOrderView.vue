<template>
  <div>
    <MerchantLogoutButton />
    <h2>订单总览</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && orders.length === 0">
      没有订单记录。
    </div>

    <div v-if="orders.length > 0">
      <h3>订单列表:</h3>
      <ul>
        <li v-for=" order in paginatedOrders" :key="order.id">
          <div class="order-item">

              <p>用户: {{ order.user }}</p>
              <p>订单时间: {{ order.date }}</p>
              <p>状态: {{ order.status }}</p>
              <p>类型: {{ order.type }}</p>
              <p>总价: {{ order.total_price }}</p>

            <el-button
                v-if="order.status === 'preparing'"
                type="success"
                @click="confirmOrder(order.id)"
            >确认订单</el-button>
          </div>
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
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";
import { ElMessage } from "element-plus";

export default {
  components: { MerchantLogoutButton },
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
      axios.get('http://127.0.0.1:8000/api/merchants/orders/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            // 反转订单数组，使最新的订单在最前面
            this.orders = response.data.reverse();
            this.loading = false;
          })
          .catch(error => {
            console.error('获取订单历史失败:', error);
            this.error = '获取订单历史失败';
            this.loading = false;
          });
    },
    confirmOrder(orderId) {
      const token = localStorage.getItem('token');
      axios.put(`http://127.0.0.1:8000/api/merchants/confirm_order/${orderId}/`, {}, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            console.log('Response data:', response.data);
            ElMessage({
              message: '订单已确认！',
              type: 'success',
            });
            this.fetchOrderHistory();
          })
          .catch(error => {
            console.error('确认订单失败：', error);
            ElMessage.error('确认订单失败！');
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

p {
  margin: 0.2rem 0;
}

.order-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.order-item p {
  margin: 0.2rem 0;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-item .order-link {
  flex-grow: 1;
}
</style>

