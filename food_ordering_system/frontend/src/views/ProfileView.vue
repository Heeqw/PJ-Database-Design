<template>
  <div class="profile">
    <h1>个人信息</h1>
    <p>用户名: {{ username }}</p>
    <p>全名: {{ full_name }}</p>
    <p>角色: {{ role }}</p>
    <p>性别: {{ gender }}</p>
    <p>手机号: {{ phone }}</p>
  </div>
</template>

<script>
export default {
  name: 'ProfileView',
  data() {
    return {
      username: '',
      full_name: '',
      role: '',
      gender: '',
      phone: ''
    };
  },
  created() {
    // 从本地存储中获取用户信息
    this.username = localStorage.getItem('username');
    this.full_name = localStorage.getItem('full_name');
    this.role = localStorage.getItem('role');
    this.gender = localStorage.getItem('gender');
    this.phone = localStorage.getItem('phone');
  }
};
</script>
<style scoped>
/* 在这里添加你的样式 */
</style>

