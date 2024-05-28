<template>
  <div class="home">
    <h1>Welcome, User {{ userId }}</h1>
    <p>This is your dashboard.</p>
    <el-button type="primary" @click="viewOrders">查看订单</el-button>
    <el-button type="primary" @click="searchMerchants">搜索商家</el-button>
    <el-button type="primary" @click="placeOrders">点单</el-button>
    <el-button type="primary" @click="goToProfile">个人信息</el-button>
</div>
</template>

<script>
export default {
  name: 'DashboardView',
  computed: {
    userId() {
      return this.$route.params.id;
    }
  },
  methods: {
    goToProfile() {
      this.$router.push({ name: 'Profile' , params: { id: this.userId }});
    },
    viewOrders() {
      this.$router.push({ name: 'Order' });
    },
    searchMerchants(){
      this.$router.push({ name: 'MerchantSearch' });
    }
  }
};
</script>


<style scoped>


</style>