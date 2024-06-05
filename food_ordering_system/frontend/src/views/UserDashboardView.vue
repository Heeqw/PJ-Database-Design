<template>
  <div class="home">
    <UserLogoutButton />
    <h1>Welcome, {{ username }}</h1> <!-- 显示用户名 -->
    <p>This is your dashboard!</p>
    <el-button type="primary" @click="viewOrders">查看订单</el-button>
    <el-button type="primary" @click="viewMessages">查看信息</el-button>
    <el-button type="primary" @click="searchMerchants">搜索商家</el-button>
    <el-button type="primary" @click="goToProfile">个人信息</el-button>
  </div>
</template>

<script>
import UserLogoutButton from '@/components/UserLogoutButton.vue';
export default {
  components: {
    UserLogoutButton // 注册登出按钮组件
  },
  name: 'DashboardView',
  data() {
    return {
      username: '',
    };
  },
  created() {
    // 从本地存储中获取用户名或用户 ID
    this.username = localStorage.getItem('username');
    // 或者 this.userid = localStorage.getItem('userid');
  },
  methods: {
    goToProfile() {
      this.$router.push({ name: 'UserProfileView', params: { id: this.$route.params.id } });
    },
    viewOrders() {
      this.$router.push({ name: 'UserOrder' });
    },
    viewMessages() {
      this.$router.push({ name: 'UserMessage' });
    },
    searchMerchants() {
      this.$router.push({ name: 'MerchantSearch' });
    },
  }
};
</script>


<style scoped>


</style>