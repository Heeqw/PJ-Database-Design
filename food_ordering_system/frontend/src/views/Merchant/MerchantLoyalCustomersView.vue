<template>
  <div>
    <MerchantLogoutButton/>
    <h2>忠实顾客消费分布（没成功）</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="error">{{ error }}</div>

    <div v-if="!loading && loyalCustomers.length === 0">
      暂无数据。
    </div>

    <div v-if="loyalCustomers.length > 0">
      <ul>
        <li v-for="(loyalCustomer, index) in loyalCustomers" :key="index">
          <h3>{{ loyalCustomer.user.username }} 的消费分布：</h3>
          <ul>
            <li v-for="dish in loyalCustomer.dishes" :key="dish.dish">
              {{ dish.dish }}: {{ dish.count }}次
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";

export default {
  components: {MerchantLogoutButton},
  data() {
    return {
      loyalCustomers: [],
      loading: true,
      error: null
    };
  },
  created() {
    const merchantId = this.$route.params.merchantId; // 从路由获取商户ID
    this.fetchLoyalCustomers(merchantId);
  },
  methods: {
    fetchLoyalCustomers(merchantId) {
      axios.get(`http://127.0.0.1:8000/api/analytics/merchant_loyal_customers/${merchantId}/`)
          .then(response => {
            this.loyalCustomers = response.data;
            this.loading = false;
          })
          .catch(error => {
            console.error('获取忠实顾客消费分布失败:', error);
            this.error = '获取数据失败';
            this.loading = false;
          });
    }
  }
};
</script>

<style scoped>
</style>
