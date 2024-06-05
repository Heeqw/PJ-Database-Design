<template>
  <div>
    <!-- 登出按钮 -->
    <el-button type="danger" @click="logout">登出</el-button>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";

export default {
  methods: {
    logout() {
      // 移除本地存储中的 token 或者其他认证信息
      localStorage.removeItem('token');
      localStorage.removeItem('merchantId');
      localStorage.removeItem('merchantPhone');
      localStorage.removeItem('merchantAddress');
      localStorage.removeItem('merchantName');
      ElMessage({message: '登出成功！', type: 'success',})
      // 重定向到登录页面
      setTimeout(() => {
        this.$router.push({ name: 'Home' });
      }, 4000);
    }
  }
};
</script>

<style scoped>
/* 样式可以根据需要自定义 */
</style>


