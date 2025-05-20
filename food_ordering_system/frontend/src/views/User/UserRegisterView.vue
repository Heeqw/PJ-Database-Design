<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="username">用户名</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <button type="submit">注册</button>
    </form>
    <div class="login-link">
      已有账号？<router-link to="/login">立即登录</router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: ''
    };
  },
  methods: {
    register() {
      axios.post('http://127.0.0.1:8000/api/users/register/', {
        username: this.username,
        password: this.password,
        email: this.email
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
      axios.post('http://127.0.0.1:8000/api/users/login/', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        const token = response.data.token;
        const user = response.data.user;
        localStorage.setItem('token', token);
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('username', user.username);
        this.$router.push(`/users/dashboard/${user.id}`);
      })
      .catch(error => {
        console.error('Login after registration failed:', error.response?.data || error);
      });
    }
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
}
.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.login-link {
  margin-top: 15px;
  text-align: center;
}
</style>