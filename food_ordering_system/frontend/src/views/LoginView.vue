<template>
  <div class="login">
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="userId">User ID:</label>
        <input type="text" v-model="userId" id="userId" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userId: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    handleLogin() {
      axios.post('http://localhost:3000/api/user_app_user/login', {
        id: this.userId,
        password: this.password
      })
          .then(response => {
            if (response.data.success) {
              this.$router.push(`/dashboard/${this.userId}`);
            } else {
              this.errorMessage = 'Invalid user ID or password';
            }
          })
          .catch(error => {
            console.error('Login error:', error);
            this.errorMessage = 'An error occurred during login';
          });
    }
  }
};
</script>

<style>
.login {
  max-width: 300px;
  margin: 50px auto;
  font-family: Arial, sans-serif;
}

.login form {
  display: flex;
  flex-direction: column;
}

.login div {
  margin-bottom: 15px;
}

.login label {
  margin-bottom: 5px;
  font-weight: bold;
}

.login input {
  padding: 8px;
  font-size: 16px;
}

.login button {
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
