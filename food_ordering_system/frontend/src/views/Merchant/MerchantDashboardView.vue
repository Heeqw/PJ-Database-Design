<template>
  <div class="home">
    <MerchantLogoutButton/>
    <h1>您好，{{ merchantName }}</h1> <!-- 显示商家名 -->
    <p>This is your dashboard!</p>
    <el-button type="primary" @click="viewOrders">查看订单</el-button>
    <el-button type="primary" @click="viewProfile">商家信息</el-button>
    <el-button type="primary" @click="viewLoyal">忠实顾客查询</el-button>
  </div>
</template>

<script>
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";


export default {
  name: 'MerchantDashboardView',
  components: {
    MerchantLogoutButton,
  },
  data() {
    return {
      merchantName: '',
    };
  },
  created() {
    // 从本地存储中获取商家名或商家 ID
    this.merchantName = localStorage.getItem('merchantName');
    // 或者 this.merchantId = localStorage.getItem('merchantId');
  },
  methods: {
    viewOrders() {
      this.$router.push({ name: 'MerchantOrder' });
    },
    viewProfile() {
      this.$router.push({ name: 'MerchantProfile', params: { id: localStorage.getItem('merchantId') } });
    },
    viewLoyal() {
      this.$router.push({ name: 'MerchantLoyalCustomers', params: { merchantId: this.merchantId } });
    },
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.el-button {
  margin: 10px;
}
</style>
