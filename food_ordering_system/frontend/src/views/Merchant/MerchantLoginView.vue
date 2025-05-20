<template>
  <div>
    <h2>Merchant Login</h2>
    <form @submit.prevent="login">
      <div style="display: block;">
        <label>用户名：</label>
        <el-input v-model="username" style="width: 240px" type="username" placeholder="Please input username" clearable/>
      </div>
      <div style="display: block;">
        <label>密码：</label>
        <el-input v-model="password" style="width: 240px" type="password" placeholder="Please input password" clearable show-password/>
      </div>
      <button type="submit">Login</button>
    </form>
    <div class="register-link">
      没有账号？<router-link to="/merchants/register">立即注册</router-link>
    </div>
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
        
        // 使用实际的商家ID而不是占位符
        this.$router.push(`/merchants/dashboard/${merchant.id}`);
      })
      .catch(error => {
        // 显示更详细的错误信息
        console.error('Merchant login failed:', error.response?.data || error);
        alert('登录失败: ' + (error.response?.data?.error || '未知错误'));
      });
    }
  }
};
</script>

<style scoped>
</style>


