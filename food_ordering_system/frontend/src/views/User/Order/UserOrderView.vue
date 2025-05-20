<template>
  <div>
    <UserLogoutButton />
    <h2>订单总览</h2>

    <!-- 过滤和排序控件 -->
    <div class="filter-container">
      <div class="filter-item">
        <label>订单状态:</label>
        <el-select v-model="filters.status" placeholder="全部状态" @change="fetchOrderHistory">
          <el-option label="全部" value=""></el-option>
          <el-option label="准备中" value="preparing"></el-option>
          <el-option label="已完成" value="completed"></el-option>
        </el-select>
      </div>
      
      <div class="filter-item">
        <label>订单类型:</label>
        <el-select v-model="filters.orderType" placeholder="全部类型" @change="fetchOrderHistory">
          <el-option label="全部" value=""></el-option>
          <el-option label="线上" value="online"></el-option>
          <el-option label="线下" value="offline"></el-option>
        </el-select>
      </div>
      
      <div class="filter-item">
        <label>日期范围:</label>
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          @change="handleDateChange"
        ></el-date-picker>
      </div>
      
      <div class="filter-item">
        <label>排序方式:</label>
        <el-select v-model="sortOption" placeholder="排序方式" @change="fetchOrderHistory">
          <el-option label="最新订单优先" value="-date"></el-option>
          <el-option label="最早订单优先" value="date"></el-option>
          <el-option label="价格从高到低" value="-total_price"></el-option>
          <el-option label="价格从低到高" value="total_price"></el-option>
        </el-select>
      </div>
    </div>

    <div v-if="loading">
      <el-skeleton :rows="3" animated />
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && orders.length === 0" class="empty-state">
      <el-empty description="没有订单记录"></el-empty>
    </div>

    <div v-if="orders.length > 0" class="orders-container">
      <h3>订单列表:</h3>
      <el-card v-for="order in orders" :key="order.id" class="order-card">
        <router-link :to="{ name: 'UserOrderDetail', params: { id: order.id } }" class="order-link">
          <div class="order-header">
            <span class="order-id">订单 #{{ order.id }}</span>
            <el-tag :type="getStatusType(order.status)">{{ getStatusText(order.status) }}</el-tag>
          </div>
          <div class="order-info">
            <p><i class="el-icon-shop"></i> 商家: {{ order.merchant_name }}</p>
            <p><i class="el-icon-date"></i> 预定时间: {{ formatDate(order.date) }} {{ order.time }}</p>
            <p><i class="el-icon-money"></i> 总价: ¥{{ order.total_price }}</p>
            <p><i class="el-icon-shopping-cart-full"></i> 类型: {{ getOrderTypeText(order.order_type) }}</p>
          </div>
        </router-link>
      </el-card>
      
      <!-- 分页控件 -->
      <div class="pagination-container">
        <el-pagination
          background
          layout="prev, pager, next, total"
          :total="totalOrders"
          :page-size="pageSize"
          :current-page="currentPage"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import UserLogoutButton from "@/components/UserLogoutButton.vue";
// import { formatDate } from '@/utils/dateFormat';

export default {
  components: { UserLogoutButton },
  data() {
    return {
      orders: [],
      loading: true,
      error: null,
      currentPage: 1,
      pageSize: 10,
      totalOrders: 0,
      filters: {
        status: '',
        orderType: '',
        startDate: '',
        endDate: ''
      },
      dateRange: [],
      sortOption: '-date'
    };
  },
  created() {
    this.fetchOrderHistory();
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    },
    getStatusType(status) {
      return status === 'completed' ? 'success' : 'warning';
    },
    getStatusText(status) {
      return status === 'completed' ? '已完成' : '准备中';
    },
    getOrderTypeText(type) {
      return type === 'online' ? '线上订单' : '线下订单';
    },
    handleDateChange() {
      if (this.dateRange && this.dateRange.length === 2) {
        this.filters.startDate = this.formatDate(this.dateRange[0]);
        this.filters.endDate = this.formatDate(this.dateRange[1]);
      } else {
        this.filters.startDate = '';
        this.filters.endDate = '';
      }
      this.fetchOrderHistory();
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchOrderHistory();
    },
    fetchOrderHistory() {
      this.loading = true;
      const token = localStorage.getItem('token');
      
      // 构建查询参数
      const params = {
        page: this.currentPage,
        page_size: this.pageSize,
        sort: this.sortOption
      };
      
      // 添加过滤条件
      if (this.filters.status) params.status = this.filters.status;
      if (this.filters.orderType) params.order_type = this.filters.orderType;
      if (this.filters.startDate) params.start_date = this.filters.startDate;
      if (this.filters.endDate) params.end_date = this.filters.endDate;
      
      axios.get('http://127.0.0.1:8000/api/orders/order_history/', {
        headers: {
          'Authorization': `Token ${token}`
        },
        params: params
      })
      .then(response => {
        this.orders = response.data.results;
        this.totalOrders = response.data.count;
        this.loading = false;
      })
      .catch(error => {
        console.error('获取订单历史失败:', error);
        this.error = '获取订单历史失败';
        this.loading = false;
      });
    }
  }
};
</script>

<style scoped>
.filter-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.filter-item label {
  margin-bottom: 5px;
  font-weight: bold;
}

.orders-container {
  margin-top: 20px;
}

.order-card {
  margin-bottom: 15px;
  transition: transform 0.3s;
}

.order-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.order-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.order-id {
  font-weight: bold;
  font-size: 1.1em;
}

.order-info p {
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.order-info i {
  margin-right: 8px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.error-message {
  color: #f56c6c;
  padding: 10px;
  background-color: #fef0f0;
  border-radius: 4px;
  margin-bottom: 15px;
}

.empty-state {
  margin: 40px 0;
}
</style>


