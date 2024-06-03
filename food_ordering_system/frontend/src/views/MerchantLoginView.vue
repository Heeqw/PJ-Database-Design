<template>
  <div>
    <h2>Merchant Login</h2>
    <form @submit.prevent="login">
      <label>Username:</label>
      <input type="text" v-model="username" required>
      <label>Password:</label>
      <input type="password" v-model="password" required>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      axios.post('http://127.0.0.1:8000/api/merchants/login/', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            const merchantId = response.data.id;
            const merchantName = response.data.name; // 获取商家名
            // 保存商家信息到本地存储
            localStorage.setItem('merchantId', merchantId);
            localStorage.setItem('merchantName', merchantName);
            // 导航到商家的仪表板或其他页面
            this.$router.push(`/merchant_dashboard/${merchantId}`);
          })
          .catch(error => {
            // 处理登录失败的响应
            console.error('Merchant login failed:', error.response.data.error);
          });
    }
  }
};
</script>

<style scoped>
/* 在这里添加你的样式 */
</style>
