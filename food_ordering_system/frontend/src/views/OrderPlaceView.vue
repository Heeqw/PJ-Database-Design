<template>
  <div>
    <UserLogoutButton />
    <h2>点单页面</h2>

    <!-- 选择就餐状态 -->
    <label for="dining-status">选择就餐状态: </label>
    <el-select v-model="orderDiningStatus" style="width: 200px" placeholder="请选择">
      <el-option label="堂食" value="dines_in"></el-option>
      <el-option label="预定" value="reservation"></el-option>
    </el-select>

    <!-- 预定日期和时间 -->
    <div v-if="orderDiningStatus === 'reservation'">
      <label for="date">选择日期: </label>
      <el-date-picker v-model="reservationDate" type="date" placeholder="选择日期"></el-date-picker>
      <label for="time">选择时间: </label>
      <el-time-picker v-model="reservationTime" placeholder="选择时间"></el-time-picker>
    </div>

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
import dayjs from 'dayjs'

export default {
  components: {UserLogoutButton},
  data() {
    return {
      dishes: [],         // 菜品列表
      quantities: {},     // 菜品数量
      merchantId: null,   // 商家ID
      orderType: 'Online',
      orderDiningStatus: null, // 就餐状态
      reservationDate: null,   // 预定日期
      reservationTime: null,   // 预定时间
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
      axios.get(`http://127.0.0.1:8000/api/merchants/${this.merchantId}/dishes/search/`)
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
      if (this.orderDiningStatus === 'reservation' && (!this.reservationDate || !this.reservationTime)) {
        ElMessage.error('预定必须选择日期和时间');
        return;
      }

      const requestData = {
        dishes: Object.keys(this.quantities).map(id => parseInt(id)),
        merchant: this.merchantId,
        order_type: this.orderType,
        quantities: this.quantities,
        order_dining_status: this.orderDiningStatus,
        date: this.orderDiningStatus === 'reservation' ? dayjs(this.reservationDate).format('YYYY-MM-DD') : null,
        time: this.orderDiningStatus === 'reservation' ? dayjs(this.reservationTime).format('HH:mm:ss') : null
      };

      axios.post('http://127.0.0.1:8000/api/orders/place_order/', requestData)
          .then(response => {
            console.log('订单提交成功:', response.data);
            ElMessage({
              message: '订单提交成功！',
              type: 'success',
            });
            // 成功提交订单后跳转个人的订单历史页面
            setTimeout(() => {
              this.$router.push({ name: 'UserOrder' });
            }, 5000);
          })
          .catch(error => {
            console.error('订单提交失败:', error);
            ElMessage.error('订单提交失败！');
          });
    }
  }
};
</script>

<style scoped>
/* 在这里添加页面样式 */
</style>
