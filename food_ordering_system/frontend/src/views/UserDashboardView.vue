<template>
  <div class="home">
    <h1>Welcome, {{ username }}</h1> <!-- 显示用户名 -->
    <p>This is your dashboard!</p>
    <el-button type="primary" @click="viewOrders">查看订单</el-button>
    <el-button type="primary" @click="searchMerchants">搜索商家</el-button>
    <el-button type="primary" @click="placeOrders">点单</el-button>
    <el-button type="primary" @click="goToProfile">个人信息</el-button>
  </div>
</template>

<script>
export default {
  name: 'DashboardView',
  data() {
    return {
      username: '',
    };
  },
  created() {
    // 从本地存储中获取用户名或用户 ID
    this.username = localStorage.getItem('username');
    // 或者 this.userid = localStorage.getItem('userid');
  },
  methods: {
    goToProfile() {
      this.$router.push({ name: 'ProfileView', params: { id: this.$route.params.id } });
    },
    viewOrders() {
      this.$router.push({ name: 'Order' });
    },
    searchMerchants() {
      this.$router.push({ name: 'MerchantSearch' });
    },
    placeOrders() {
        this.$router.push({ name: 'PlaceOrder' });
    }
  }
};
</script>


<style scoped>


</style>