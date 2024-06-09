<template>
  <div>
    <MerchantLogoutButton />
    <h1>菜品详情</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <p>名称：{{ dish.name }}</p>
      <p>类别：{{ dish.category }}</p>
      <p>价格：{{ dish.price }}</p>
      <el-input type="number" style="width: 120px" v-model="newPrice" placeholder="输入新价格" @input="checkPrice"/>
      <el-button type="primary" @click="updatePrice">修改价格</el-button>
      <p><img :src="dish.image_url" alt="菜品图片"></p>
    </div>
  </div>
</template>

<script>
import MerchantLogoutButton from "@/components/MerchantLogoutButton.vue";
import { ElMessage } from "element-plus";

export default {
  components: { MerchantLogoutButton },
  data() {
    return {
      loading: true,
      dish: null,
      error: null,
      newPrice: null // 新价格的数据绑定
    };
  },
  mounted() {
    this.fetchDishDetails();
  },
  methods: {
    fetchDishDetails() {
      const dishId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/dishes/${dishId}/`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.dish = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = '获取菜品详情失败';
            console.error('获取菜品详情失败:', error);
          });
    },
    updatePrice() {
      if (this.newPrice <= 0) {
        this.newPrice = 1; // 如果价格小于等于 0，将自动置为 1
        ElMessage.warning('价格不能小于等于 0'); // 显示警告消息
        return;
      }

      const dishId = this.$route.params.id;
      const token = localStorage.getItem('token'); // 假设 token 存储在 localStorage 中
      fetch(`http://127.0.0.1:8000/api/merchants/update_dish_price/${dishId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${token}`
        },
        body: JSON.stringify({
          new_price: parseFloat(this.newPrice)
        })
      })
          .then(response => {
            if (response.ok) {
              alert('价格已更新');
              this.fetchDishDetails(); // 更新后重新获取菜品详情
            } else {
              throw new Error('价格更新失败');
            }
          })
          .catch(error => {
            console.error('价格更新失败:', error);
            alert('价格更新失败');
          });
    },
    checkPrice() {
      if (this.newPrice <= 0) {
        this.newPrice = 1; // 如果价格小于等于 0，将自动置为 1
        ElMessage.warning('价格不能小于等于 0'); // 显示警告消息
      }
    }
  }
};
</script>

<style>
.details p {
  margin-bottom: 10px;
}
img {
  width: 100%; /* 根据需要调整 */
  max-width: 400px; /* 根据需要调整 */
  height: auto;
  display: block;
  margin: 0 auto;
}
</style>
