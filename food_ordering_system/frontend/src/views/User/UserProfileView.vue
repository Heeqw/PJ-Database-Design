<template>
  <div class="profile">
    <UserLogoutButton />
    <el-button type="primary" @click="viewActivities">活跃度查看</el-button>
    <el-button type="primary" @click="viewDemograhics">群体特征查看</el-button>

    <h1>个人信息</h1>
    <p>用户名: {{ user.username }}</p>
    <p>全名: {{ user.full_name }}</p>
    <p>角色: {{ user.role }}</p>
    <p v-if="user.role === 'student'">学生编号: {{ user.student_id }}</p>
    <p v-if="user.role === 'staff'">员工编号: {{ user.staff_id }}</p>
    <p>性别: {{ user.gender }}</p>
    <p>年龄: {{ user.age }}</p>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  name: 'ProfileView',
  components: {UserLogoutButton},
  data() {
    return {
      user: {}
    };
  },
  created() {
    // 从本地存储中获取用户信息
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
      this.user = user;
    }
  },
  methods:{
    viewActivities() {
      this.$router.push({ name: 'UserActivities' });
    },
    viewDemograhics() {
      this.$router.push({ name: 'UserDemographics' });
    },
  }
};
</script>

<style scoped>

</style>
