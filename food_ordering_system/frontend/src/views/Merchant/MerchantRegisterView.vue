<template>
  <div>
    <h2>商家注册</h2>
    <form @submit.prevent="register">
      <div style="display: block;">
        <label>商家名称：</label>
        <el-input v-model="name" style="width: 240px" placeholder="请输入商家名称" clearable/>
      </div>
      <div style="display: block;">
        <label>地址：</label>
        <el-input v-model="address" style="width: 240px" placeholder="请输入地址" clearable/>
      </div>
      <div style="display: block;">
        <label>联系电话：</label>
        <el-input v-model="phone" style="width: 240px" placeholder="请输入联系电话" clearable/>
      </div>
      <div style="display: block;">
        <label>用户名：</label>
        <el-input v-model="username" style="width: 240px" placeholder="请输入用户名" clearable/>
      </div>
      <div style="display: block;">
        <label>密码：</label>
        <el-input v-model="password" style="width: 240px" type="password" placeholder="请输入密码" clearable show-password/>
      </div>
      <button type="submit">注册</button>
    </form>
    <div class="login-link">
      已有账号？<router-link to="/merchants/login">立即登录</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      address: '',
      phone: '',
      username: '',
      password: ''
    };
  },
  methods: {
    register() {
      axios.post('http://127.0.0.1:8000/api/merchants/create/', {
        name: this.name,
        address: this.address,
        phone: this.phone,
        username: this.username,
        password: this.password
      })
      .then(response => {
        console.log('Registration successful:', response.data);
        // 注册成功后自动登录
        this.login();
      })
      .catch(error => {
        console.error('Registration failed:', error.response?.data || error);
      });
    },
    login() {
      axios.post('http://127.0.0.1:8000/api/merchants/login/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        const token = response.data.token;
        const merchant = response.data.merchant;
        localStorage.setItem('token', token);
        localStorage.setItem('merchantId', merchant.id);
        localStorage.setItem('merchantName', merchant.name);
        localStorage.setItem('merchantAddress', merchant.address);
        localStorage.setItem('merchantPhone', merchant.phone);
        this.$router.push(`/merchants/dashboard/${merchant.id}`);
      })
      .catch(error => {
        console.error('Login after registration failed:', error.response?.data || error);
      });
    }
  }
};
</script>

<style scoped>
div {
  margin-bottom: 15px;
}
.login-link {
  margin-top: 15px;
  text-align: center;
}
</style>