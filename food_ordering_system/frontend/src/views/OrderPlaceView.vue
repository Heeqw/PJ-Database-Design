<template>
  <div>
    <h2>下单页面（示例，未完成）</h2>
    <label for="item">商品名称：</label>
    <input type="text" id="item" v-model="item">

    <label for="quantity">数量：</label>
    <input type="number" id="quantity" v-model="quantity">

    <button @click="placeOrder">下单</button>

    <div v-if="loading">正在提交订单...</div>

    <div v-if="success">订单提交成功！</div>

    <div v-if="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      item: '',
      quantity: 1,
      loading: false,
      success: false,
      error: null
    };
  },
  methods: {
    placeOrder() {
      this.loading = true;
      this.error = null;
      axios.post('http://localhost:8000/api/orders/place_order/', {
        item: this.item,
        quantity: this.quantity
      })
          .then(response => {
            this.loading = false;
            this.success = true;
            console.log(response.data); // 可以在控制台查看服务器返回的数据
          })
          .catch(error => {
            this.loading = false;
            this.error = '下单失败，请稍后再试。';
            console.error('下单失败:', error);
          });
    }
  }
};
</script>
