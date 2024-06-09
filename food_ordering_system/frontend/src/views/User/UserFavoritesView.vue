<template>
  <div class="home">
    <h1>收藏内容</h1>
    <el-button type="primary" @click="goToFavoriteMerchants">收藏的商家</el-button>
    <el-button type="primary" @click="goToFavoritesDishes">收藏的菜品</el-button>
  </div>
</template>

<script>
export default {

  methods: {
    goToFavoriteMerchants() {
      this.$router.push({ name: 'FavoriteMerchants' });
    },
    goToFavoritesDishes() {
      this.$router.push({ name: 'FavoriteDishes' });
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}
.login-button {
  margin-right: 10px;
}
</style>
