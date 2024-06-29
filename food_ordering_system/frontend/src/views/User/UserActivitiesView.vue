<template>
  <div>
    <UserLogoutButton />
    <h2>用户活跃度分析</h2>

    <!-- 周活跃度表格 -->
    <h3>每周点餐次数变化</h3>
    <table>
      <thead>
        <tr>
          <th>周</th>
          <th>点餐次数</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(activity, index) in weeklyActivity" :key="index">
          <td>{{ activity.week }}</td>
          <td>{{ activity.count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 月活跃度表格 -->
    <h3>每月点餐次数变化</h3>
    <table>
      <thead>
        <tr>
          <th>月份</th>
          <th>点餐次数</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(activity, index) in monthlyActivity" :key="index">
          <td>{{ activity.month }}</td>
          <td>{{ activity.count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 时间段活跃度表格 -->
    <h3>不同时间段点餐总次数统计</h3>
    <table>
      <thead>
        <tr>
          <th>时间段</th>
          <th>点餐次数</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(activity, index) in timeActivity" :key="index">
          <td>{{ activity.hour }}:00</td>
          <td>{{ activity.count }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      weeklyActivity: [],
      monthlyActivity: [],
      timeActivity: [], // 修改这里，直接展示timeActivity
      loading: true,
      error: null
    };
  },
  created() {
    this.fetchUserActivity();
  },
  methods: {
    fetchUserActivity() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:8000/api/analytics/user_activity_analysis/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      })
        .then(response => {
          this.weeklyActivity = response.data.weekly_activity;
          this.monthlyActivity = response.data.monthly_activity;
          this.timeActivity = response.data.time_activity;

          // 检查数据
          console.log("Weekly Activity:", this.weeklyActivity);
          console.log("Monthly Activity:", this.monthlyActivity);
          console.log("Time Activity:", this.timeActivity);

          this.loading = false;
        })
        .catch(error => {
          console.error('获取用户活跃度失败:', error);
          this.error = '获取用户活跃度失败';
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped>
h3 {
  margin-top: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}
table th, table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>
