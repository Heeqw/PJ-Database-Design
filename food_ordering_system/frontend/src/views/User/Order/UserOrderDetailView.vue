<template>
  <div>
    <UserLogoutButton />
    <h2>订单详情</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && orderDetails.length === 0">
      没有找到订单详情。
    </div>

    <div v-if="orderDetails.length > 0">
      <h3>订单 ID: {{ $route.params.id }}</h3>
      <ul>
        <li v-for="detail in orderDetails" :key="detail.id">
          <p>菜品名称: {{ detail.dish.name }}</p>
          <p>数量: {{ detail.quantity }}</p>
          <p>价格: {{ detail.price }}</p>
          <el-rate v-model="detail.rating" :disabled="detail.reviewed" :max="5" allow-half></el-rate>
          <el-input v-model="detail.comment" :disabled="detail.reviewed" placeholder="请输入评论"></el-input>
          <el-button v-if="!detail.reviewed" @click="submitReview(detail)">确认评价</el-button>
          <p v-else>已评价: 评分 {{ detail.rating }}, 评论: {{ detail.comment }}</p>
        </li>
      </ul>
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
      orderDetails: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchOrderDetails();
  },
  methods: {
    fetchOrderDetails() {
      const orderId = this.$route.params.id;
      const token = localStorage.getItem('token');
      axios.get(`http://127.0.0.1:8000/api/orders/order_detail/${orderId}/`, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            // 这里假设从后端返回的数据中已经包含了reviewed、rating和comment的信息
            this.orderDetails = response.data.map(detail => ({
              ...detail,
              reviewed: detail.reviewed || false,  // 假设后端返回的数据中有reviewed字段
              rating: detail.rating || null,       // 假设后端返回的数据中有rating字段
              comment: detail.comment || ''        // 假设后端返回的数据中有comment字段
            }));
            this.loading = false;
          })
          .catch(error => {
            console.error('获取订单详情失败:', error);
            this.error = '获取订单详情失败';
            this.loading = false;
          });
    },
    submitReview(detail) {
      const dishId = detail.dish.id;
      const token = localStorage.getItem('token');
      const data = {
        rating: detail.rating,
        comment: detail.comment
      };
      axios.post(`http://127.0.0.1:8000/api/dishes/${dishId}/add_review/`, data, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            console.log('评价已提交:', response.data);
            detail.reviewed = true;
          })
          .catch(error => {
            console.error('提交评价失败:', error);
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
  border: 1px solid #ddd;
  width: 300px; /* 设置每个菜品显示框的宽度 */
}
</style>