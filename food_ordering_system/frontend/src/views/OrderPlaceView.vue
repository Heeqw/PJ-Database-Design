<template>
  <div>
    <UserLogoutButton />
    <h2>点单页面</h2>

    <!-- 菜品列表 -->
    <div v-for="dish in dishes" :key="dish.id">
      <p>{{ dish.name }}</p>
      <label>数量:  </label>
      <el-input v-model="quantities[dish.id]" style="width: 200px"
                type="number" placeholder="Please input number"
                @input="validateQuantity(dish.id)"/>
    </div>

    <!-- 提交按钮 -->
    <el-button type="primary" class="order-place-button" @click="placeOrder">我要下单</el-button>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: {UserLogoutButton},
  data() {
    return {
      dishes: [],       // 菜品列表
      quantities: {},   // 菜品数量
      merchantId: null, // 商家ID
      orderType: 'Online',
      status: 'Preparing'
    };
  },
  created() {
    // 获取商家ID
    this.merchantId = this.$route.params.id;
    // 获取菜品列表
    this.fetchDishes();
  },
  methods: {
    // 获取菜品列表
    fetchDishes() {
      axios.get(`http://127.0.0.1:8000/api/dishes/search/${this.merchantId}/`)
          .then(response => {
            this.dishes = response.data;
            // 初始化菜品数量为1
            this.dishes.forEach(dish => {
              this.$set(this.quantities, dish.id, 1);
            });
          })
          .catch(error => {
            console.error('获取菜品列表失败:', error);
          });
    },
    // 验证数量
    validateQuantity(dishId) {
      if (this.quantities[dishId] < 0) {
        ElMessage.error('数量不能为负数！');
        this.quantities[dishId] = 0; // 将负数重置为0
      }
    },
    // 提交订单
    placeOrder() {
      const requestData = {
        dishes: Object.keys(this.quantities).map(id => parseInt(id)),
        merchant: this.merchantId,
        order_type: this.orderType,
        quantities: this.quantities
      };

      axios.post('http://127.0.0.1:8000/api/orders/place_order/', requestData)
          .then(response => {
            console.log('订单提交成功:', response.data);
            ElMessage({
              message: '订单提交成功！',
              type: 'success',
            })
            // 成功提交订单后跳转个人的订单历史页面
            setTimeout(() => {
              this.$router.push({ name: 'UserOrder' });
            }, 5000);
          })
          .catch(error => {
            console.error('订单提交失败:', error);
            // 这里可以添加处理失败情况的逻辑
          });
    }
  }
};
</script>

<style scoped>
/* 在这里添加页面样式 */

</style>
