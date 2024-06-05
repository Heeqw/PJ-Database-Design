<template>
  <div>
    <UserLogoutButton />
    <h2>用户信息页面</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="!loading && messages.length === 0">
      没有消息。
    </div>

    <div v-if="messages.length > 0">
      <h3>消息列表:</h3>
      <ul>
        <li v-for="message in messages" :key="message.id">
          <p>{{ message.message }}</p>
          <!-- 其他消息信息 -->
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: {UserLogoutButton},
  data() {
    return {
      messages: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    fetchMessages() {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      console.log('Token:', token);
      axios.get('http://127.0.0.1:8000/api/messages/list/')
          .then(response => {
            console.log('Response data:', response.data); // 调试：打印响应数据
            this.messages = response.data;
            this.loading = false;
          })
          .catch(error => {
            console.error('获取信息失败:', error);
            this.error = '获取信息失败';
            this.loading = false;
          });
    }
  }
};
</script>

<style scoped>
/* 添加一些样式使页面更好看 */
ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
}

p {
  margin: 0.2rem 0;
}
</style>
