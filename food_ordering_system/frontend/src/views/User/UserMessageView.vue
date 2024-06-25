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
        <li v-for="message in paginatedMessages" :key="message.id" class="message-item">
          <p>{{ message.message }}</p>
          <span v-if="message.read" class="read-icon">已读</span>
          <span v-else class="unread-icon">未读</span>
          <el-button v-if="!message.read" type="success" @click="markAsRead(message.id)">标记为已读</el-button>
        </li>
      </ul>
      <div>
        <p>共 {{ messages.length }} 条消息</p>
        <p>当前页 {{ currentPage }} / {{ totalPages }}</p>
        <button @click="changePage(-1)" :disabled="currentPage === 1">上一页</button>
        <button @click="changePage(1)" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      messages: [],
      loading: true,
      error: null,
      currentPage: 1,
      pageSize: 3
    };
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    fetchMessages() {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      console.log('Token:', token);
      axios.get('http://127.0.0.1:8000/api/messages/messages/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
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
    },
    markAsRead(messageId) {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      axios.put(`http://127.0.0.1:8000/api/messages/messages/${messageId}/read/`, {}, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            console.log('消息已标记为已读:', response.data); // 调试：打印响应数据
            // 更新消息的已读状态
            const updatedMessages = this.messages.map(message => {
              if (message.id === response.data.id) {
                return response.data;
              }
              return message;
            });
            this.messages = updatedMessages;
          })
          .catch(error => {
            console.error('标记为已读失败:', error);
            this.error = '标记为已读失败';
          });
    },
    changePage(pageOffset) {
      this.currentPage += pageOffset;
    }
  },
  computed: {
    paginatedMessages() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      return this.messages.slice(startIndex, startIndex + this.pageSize);
    },
    totalPages() {
      return Math.ceil(this.messages.length / this.pageSize);
    }
  }
};
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
  position: relative; /* 相对定位，用于定位图标和按钮 */
}

p {
  margin: 0.2rem 0;
}

.read-icon {
  color: green;
  position: absolute;
  top: 10px;
  right: 10px;
}

.unread-icon {
  color: red;
  position: absolute;
  top: 10px;
  right: 10px;
}

.el-button {
  margin-top: 10px;
}
</style>
