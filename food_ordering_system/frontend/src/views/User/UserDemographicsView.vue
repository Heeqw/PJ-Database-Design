<template>
  <div>
    <UserLogoutButton />
    <h2>用户群体特征分析</h2>

    <div v-if="roleDistribution.length > 0">
      <div class="chart" ref="roleChart"></div>
    </div>

    <div v-if="ageDistribution.length > 0">
      <div class="chart" ref="ageChart"></div>
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
      roleDistribution: [],
      ageDistribution: [],
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchUserDemographics();
  },
  methods: {
    fetchUserDemographics() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:8000/api/analytics/user_demographics_analysis/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
          .then(response => {
            this.roleDistribution = response.data.role_distribution;
            this.ageDistribution = response.data.age_distribution;
            this.loading = false;

            // 在数据加载后初始化图表
            this.$nextTick(() => {
              this.initRoleChart();
              this.initAgeChart();
            });
          })
          .catch(error => {
            console.error('获取用户群体特征失败:', error);
            this.error = '获取用户群体特征失败';
            this.loading = false;
          });
    },
    initRoleChart() {
      const roleChartDom = this.$refs.roleChart;
      const roleChart = echarts.init(roleChartDom);

      // 准备角色数据
      const roleData = this.roleDistribution.map(item => ({
        name: item.role,
        value: item.count
      }));

      const roleOption = {
        title: {
          text: '用户角色分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.roleDistribution.map(item => item.role)
        },
        series: [
          {
            name: '角色',
            type: 'pie',
            radius: '50%',
            center: ['50%', '60%'],
            data: roleData,
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

      roleChart.setOption(roleOption);
    },
    initAgeChart() {
      const ageChartDom = this.$refs.ageChart;
      const ageChart = echarts.init(ageChartDom);

      // 准备年龄数据
      const ageData = this.ageDistribution.map(item => ({
        name: `${item.age}岁`,
        value: item.count
      }));

      const ageOption = {
        title: {
          text: '用户年龄分布',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.ageDistribution.map(item => `${item.age}岁`)
        },
        series: [
          {
            name: '年龄',
            type: 'pie',
            radius: '50%',
            center: ['50%', '60%'],
            data: ageData,
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

      ageChart.setOption(ageOption);
    }
  }
};
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
