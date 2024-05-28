<template>
  <div>
    <h2>商家搜索</h2>
    <input type="text" v-model="searchQuery" placeholder="输入商家名称">
    <button @click="search">搜索</button>
    <div v-if="searchResult.length > 0">
      <ul>
        <li v-for="merchant in searchResult" :key="merchant.id">
          {{ merchant.name }} - {{ merchant.address }} - {{ merchant.phone }}
        </li>
      </ul>
    </div>
    <div v-else>
      没有找到匹配的商家信息。
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      searchResult: [],
    };
  },
  methods: {
    search() {
      axios.get('http://localhost:3000/api/merchant_app_merchant/', {
        params: {
          q: this.searchQuery
        }
      })
          .then(response => {
            this.searchResult = response.data;
          })
          .catch(error => {
            console.error('Error fetching merchant data:', error);
          });
    }
  }
}
</script>


<style scoped>
/* 样式可以根据需要进行调整 */

</style>
