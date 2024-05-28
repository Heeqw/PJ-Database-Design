<template>
  <div class="home">
    <h1>校园点餐系统</h1>
    <el-button type="primary" class="login-button" @click="goToLogin">登录</el-button>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  methods: {
    goToLogin() {
      this.$router.push({ name: 'Login' });
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}

</style>
