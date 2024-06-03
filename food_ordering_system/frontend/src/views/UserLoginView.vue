<template>
  <div>
    <h2>Login</h2>
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
      axios.post('http://127.0.0.1:8000/api/users/login/', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            //const token = response.data.token;
            const username = response.data.user.username; // 获取用户名
            const userid = response.data.user.id;
            const gender = response.data.gender;
            const full_name = response.data.user.full_name;
            const phone = response.data.user.phone;
            const role = response.data.user.role;
            //localStorage.setItem('token', token);
            localStorage.setItem('username', username); // 存储用户名
            localStorage.setItem('userid',userid);
            localStorage.setItem('gender', gender);
            localStorage.setItem('full_name',full_name);
            localStorage.setItem('phone', phone);
            localStorage.setItem('role', role);
            this.$router.push(`/user_dashboard/${userid}`);
          })
          .catch(error => {
            // 处理登录失败的响应
            console.error('Login failed:', error.response.data.error);
          });
    }
  }
};
</script>

<style scoped>
/* 在这里添加你的样式 */
</style>