<template>
  <div class="home">
    <h1>校园点餐系统</h1>
    <el-button type="primary" class="login-button" @click="goToUserLogin">用户登录</el-button>
    <el-button type="primary" class="login-button" @click="goToMerchantLogin">商家登录</el-button>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    goToUserLogin() {
      this.$router.push({ name: 'UserLogin' });
    },
    goToMerchantLogin() {
      this.$router.push({ name: 'MerchantLogin' });
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}
.login-button {
  margin-right: 10px;
}
</style>
