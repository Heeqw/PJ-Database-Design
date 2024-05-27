<template>
  <div class="merchant-details">
    <h1>{{ merchant.name }}</h1>
    <div>
      <p><strong>Address:</strong> {{ merchant.address }}</p>
      <p><strong>Phone:</strong> {{ merchant.phone }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      merchant: {}
    };
  },
  created() {
    this.fetchMerchantData();
  },
  watch: {
    // 监听路由参数 id 的变化，当变化时重新获取商家数据
    '$route.params.id': 'fetchMerchantData'
  },
  methods: {
    fetchMerchantData() {
      const merchantId = this.$route.params.id;
      axios.get(`http://localhost:3000/api/merchant_app_merchant/${merchantId}`)
          .then(response => {
            this.merchant = response.data[0]; // 假设返回的数据只有一个商家
          })
          .catch(error => {
            console.error('获取商家数据时出错:', error);
          });
    }
  }
};
</script>

<style>
.merchant-details {
  font-family: Arial, sans-serif;
}
.details p {
  margin-bottom: 10px;
}
</style>
