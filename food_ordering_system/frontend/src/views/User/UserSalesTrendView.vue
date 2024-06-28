<template>
  <div>
    <UserLogoutButton />
    <h2>商家销售趋势</h2>

    <div v-if="loading">加载中...</div>

    <div v-if="error">{{ error }}</div>

    <div>
      <label for="period">选择时间范围：</label>
      <select v-model="period" @change="fetchSalesTrends" class="large-select">
        <option value="week">周</option>
        <option value="month">月</option>
        <option value="year">年</option>
      </select>

      <label for="interval">选择时间间隔：</label>
      <select v-model="interval" @change="fetchSalesTrends" class="large-select">
        <option value="day">日</option>
        <option value="week">周</option>
        <option value="month">月</option>
      </select>
    </div>

    <div v-if="!loading && salesTrends.length === 0">
      没有销售趋势记录。
    </div>

    <div v-if="salesTrends.length > 0">
      <h3>销售趋势列表:</h3>
      <div v-for="(trend, index) in salesTrends" :key="trend.dish.id" class="trend-item">
        <h4>{{ trend.dish.name }}</h4>
        <div :ref="'chart-' + index" class="chart"></div>
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
      salesTrends: [],
      loading: true,
      error: null,
      merchantId: null,
      period: 'month', // 默认时间范围
      interval: 'day'  // 默认时间间隔
    };
  },
  created() {
    // 从路由参数中获取商家ID
    this.merchantId = this.$route.params.id;
    // 根据商家ID获取商家信息，如果需要可以在这里加载商家信息
    this.fetchSalesTrends();
  },
  methods: {
    fetchSalesTrends() {
      const token = localStorage.getItem('token'); // 从本地存储中获取token
      axios.get(`http://127.0.0.1:8000/api/analytics/dish_sales_trend/${this.merchantId}/`, {
        headers: {
          'Authorization': `Token ${token}`
        },
        params: {
          period: this.period,
          interval: this.interval
        }
      })
          .then(response => {
            this.salesTrends = response.data;
            this.loading = false;
            this.$nextTick(() => {
              this.salesTrends.forEach((trend, index) => {
                this.initChart(trend, index);
              });
            });
          })
          .catch(error => {
            console.error('获取销售趋势信息失败:', error);
            this.error = '获取销售趋势信息失败';
            this.loading = false;
          });
    },
    initChart(trend, index) {
      const chartDom = this.$refs[`chart-${index}`][0]; // 确保获取正确的 DOM 元素
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: `${trend.dish.name} 的销售趋势`
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: trend.sales_trend.map(item => item.interval)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '销售数量',
            type: 'line',
            data: trend.sales_trend.map(item => item.sales),
            areaStyle: {}
          }
        ]
      };
      myChart.setOption(option);
    }
  }
};
</script>

<style scoped>
h3 {
  margin-top: 20px;
}
select {
  margin-right: 10px;
}
.large-select {
  font-size: 1.2em;
  padding: 5px;
  margin-right: 10px;
}
.trend-item {
  margin-bottom: 2rem;
}

.chart {
  width: 100%;
  height: 400px;
}
</style>

