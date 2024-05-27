<template>
  <div class="profile">
    <h1>User Profile</h1>
    <div>
      <p><strong>Username:</strong> {{ userProfile.username }}</p>
      <p><strong>Email:</strong> {{ userProfile.email }}</p>
      <p><strong>Role:</strong> {{ userProfile.role }}</p>
      <p><strong>Full Name:</strong> {{ userProfile.full_name }}</p>
      <p><strong>Gender:</strong> {{ userProfile.gender }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userProfile: {}
    };
  },
  created() {
    this.fetchUserProfile();
  },
  watch: {
    // 监听路由参数 id 的变化，当变化时重新获取商家数据
    '$route.params.id': 'fetchUserData'
  },
  methods: {
    fetchUserProfile() {
      const userId = this.$route.params.id;
      axios.get(`http://localhost:3000/api/user_app_user/${userId}`)
          .then(response => {
            this.userProfile = response.data[0];
          })
          .catch(error => {
            console.error('Error fetching user profile:', error);
          });
    }
  }
};
</script>

<style>
.profile {
  font-family: Arial, sans-serif;
  margin: 20px;
}
</style>
