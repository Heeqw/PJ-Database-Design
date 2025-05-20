<template>
  <div>
    <MerchantLogoutButton />
    <h2>添加菜品</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">菜品名称:</label>
        <input type="text" v-model="form.name" id="name" required>
      </div>
      <div>
        <label for="price">价格:</label>
        <input type="number" v-model="form.price" id="price" required @change="validatePrice">
      </div>
      <div>
        <label for="category">类别:</label>
        <input type="text" v-model="form.category" id="category" required>
      </div>
      <div>
        <label for="description">描述:</label>
        <input type="text" v-model="form.description" id="description" required>
      </div>
      <div>
      <label for="ingredients">原料:</label>
      <input type="text" v-model="form.ingredients" id="ingredients" required>
      </div>
      <div>
        <label for="nutrition_info">营养成分:</label>
        <input type="text" v-model="form.nutrition_info" id="nutrition_info" required>
      </div>

      <div>
        <label for="image_url">图片 URL（可去此网站生成：https://sm.ms/）:</label>
        <input type="text" v-model="form.image_url" id="image_url" required>
      </div>
      <button type="submit">提交</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">菜品已成功添加！</div>
  </div>
</template>

<script>
import axios from 'axios';
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";
import { ElMessage } from 'element-plus'; // 引入 Element Plus 消息组件

export default {
  components: { MerchantLogoutButton },
  data() {
    return {
      form: {
        name: '',
        price: '',
        category: '',
        image_url: ''
      },
      error: null,
      success: false
    };
  },
  methods: {
    validatePrice() {
      if (this.form.price <= 0) {
        this.form.price = 1; // 如果价格小于等于 0，将自动置为 1
        ElMessage.warning('价格不能小于等于 0'); // 显示警告消息
      }
    },
    submitForm() {
      if (this.form.price <= 0) {
        this.error = '价格不能小于等于 0';
        ElMessage.error('价格不能小于等于 0');
        return;
      }

      // 使用正确的token变量名
      const token = localStorage.getItem('token'); // 不是merchantToken
      axios.post('http://127.0.0.1:8000/api/merchants/create_dish/', this.form, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
      .then(response => {
        console.log('成功添加菜品:', response.data);
        this.success = true;
        this.error = null;
        this.form = {
          name: '',
          price: '',
          category: '',
          image_url: ''
        };
      })
      .catch(error => {
        this.success = false;
        if (error.response) {
          this.error = error.response.data;
          console.error('添加菜品失败:', error.response.data);
        } else {
          this.error = '请求失败，请稍后重试。';
        }
      });
    }
  }
};
</script>

<style scoped>
.error {
  color: red;
}
.success {
  color: green;
}
</style>

