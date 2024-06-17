<template>
  <div>
    <h2>Merchant Login</h2>
    <form @submit.prevent="login">
      <div style="display: block;">
        <label>Username:</label>
        <el-input v-model="username" style="width: 240px" type="username" placeholder="Please input username" clearable/>
      </div>
      <div style="display: block;">
        <label>Password:</label>
        <el-input v-model="password" style="width: 240px" type="password" placeholder="Please input password" clearable show-password/>
      </div>
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
            const token = response.data.token;
            const merchant = response.data.merchant;
            // 保存商家信息到本地存储
            localStorage.setItem('token', token);
            localStorage.setItem('merchantId', merchant.id);
            localStorage.setItem('merchantName', merchant.name);
            localStorage.setItem('merchantAddress', merchant.address);
            localStorage.setItem('merchantPhone', merchant.phone);
            // 导航到商家的仪表板或其他页面
            this.$router.push(`/merchants/dashboard/${merchant.id}`);
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
