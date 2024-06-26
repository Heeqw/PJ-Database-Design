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
      <tr v-for="(activity, index) in combinedTimeActivity" :key="index">
        <td>{{ activity.time }}</td>
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
      timeActivity: [],
      combinedTimeActivity: [], // 新增一个数组用于存放合并后的时间段统计
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

            // 调用方法合并相同时间段的点餐次数
            this.combineTimeActivity();

            this.loading = false;
          })
          .catch(error => {
            console.error('获取用户活跃度失败:', error);
            this.error = '获取用户活跃度失败';
            this.loading = false;
          });
    },
    combineTimeActivity() {
      // 使用一个对象来临时存放合并后的数据
      const combined = {};

      // 遍历时间段活跃度数据
      this.timeActivity.forEach(activity => {
        // 获取时间段的小时部分，比如 "2024-06-05T06:00:00" -> "06"
        const hour = new Date(activity.hour).getHours().toString();

        // 如果该时间段的数据已经存在，则累加点餐次数，否则初始化
        if (combined[hour]) {
          combined[hour].count += activity.count;
        } else {
          combined[hour] = {
            time: `${hour}:00`,
            count: activity.count
          };
        }
      });

      // 将对象转换为数组并赋值给 combinedTimeActivity
      this.combinedTimeActivity = Object.values(combined);
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
  width: 50%; /* 设置列宽度为50% */
}
</style>

