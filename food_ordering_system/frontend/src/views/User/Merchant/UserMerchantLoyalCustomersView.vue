<template>
  <div>
    <UserLogoutButton />
    <h2>忠实顾客消费分布</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="error">{{ error }}</div>

    <div v-if="!loading && loyalCustomers.length === 0">
      没有忠实顾客记录。
    </div>

    <div v-if="loyalCustomers.length > 0">
      <h3>忠实顾客列表:</h3>
      <div v-for="(customer, index) in loyalCustomers" :key="customer.user.id" class="customer-item">
        <h4>{{ customer.user.full_name }}</h4>
        <div :ref="`chart-${index}`" class="chart"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      loyalCustomers: [],
      loading: true,
      error: null,
      merchantId: null
    };
  },
  created() {
    // 从路由参数中获取商家ID
    this.merchantId = this.$route.params.id;
    // 根据商家ID获取商家信息，如果需要可以在这里加载商家信息
    this.fetchLoyalCustomers();
  },
  methods: {
    fetchLoyalCustomers() {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      axios.get(`http://127.0.0.1:8000/api/analytics/merchant_loyal_customers/${this.merchantId}/`, {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            this.loyalCustomers = response.data;
            this.loading = false;
            this.$nextTick(() => {
              this.loyalCustomers.forEach((customer, index) => {
                this.initChart(customer, index);
              });
            });
          })
          .catch(error => {
            console.error('获取忠实顾客信息失败:', error);
            this.error = '获取忠实顾客信息失败';
            this.loading = false;
          });
    },
    initChart(customer, index) {
      const chartDom = this.$refs[`chart-${index}`][0]; // 确保获取正确的 DOM 元素
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: `${customer.user.full_name} 的消费分布`
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '5%',
          left: 'center'
        },
        series: [
          {
            name: '消费次数',
            type: 'pie',
            radius: '50%',
            data: customer.dishes.map(dish => ({ value: dish.count, name: `菜品 ${dish.dish}` })), // 使用菜品份数
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      myChart.setOption(option);
    }
  }
};
</script>


<style scoped>
.customer-item {
  margin-bottom: 2rem;
}

.chart {
  width: 100%;
  height: 400px;
}
</style>
