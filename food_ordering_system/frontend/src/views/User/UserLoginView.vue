<template>
  <div class="login-container">
    <div>
      <h2>用户登录</h2>
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
    </div>
    <div class="register-link">
      没有账号？<router-link to="/register">立即注册</router-link>
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
      axios.post('http://127.0.0.1:8000/api/users/login/', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            const token = response.data.token;
            const user = response.data.user;
            console.log('Token:', token); // 打印Token以供调试
            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(user));
            localStorage.setItem('username', user.username);
            this.$router.push(`/users/dashboard/${user.id}`);
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
.register-link {
  margin-top: 15px;
  text-align: center;
}
</style>

