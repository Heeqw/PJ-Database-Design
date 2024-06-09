<template>
  <div>
    <UserLogoutButton />
    <h1>Dish Details</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Name: {{ dish.name }}</p>
      <p>Price: {{ dish.price }}</p>
      <p><img :src="dish.image_url" alt="Dish Image"></p>
      <h2>Price History</h2>
      <div v-if="priceHistory.length === 0">No price history available.</div>
      <ul v-else>
        <li v-for="history in priceHistory" :key="history.id">
          Old Price: {{ history.old_price }}, New Price: {{ history.new_price }}, Changed At: {{ history.changed_at }}
        </li>
      </ul>
      <h2>Reviews</h2>
      <div v-if="dish.reviews.length === 0">No reviews available.</div>
      <ul v-else>
        <li v-for="review in dish.reviews" :key="review.id">
          <p>User: {{ review.user }}</p>
          <p>Rating: {{ review.rating }}</p>
          <p>Comment: {{ review.comment }}</p>
          <p>Created At: {{ review.created_at }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: { UserLogoutButton },
  data() {
    return {
      loading: true,
      dish: null,
      priceHistory: [],
      error: null
    };
  },
  mounted() {
    this.fetchDishDetails();
    this.fetchPriceHistory();
  },
  methods: {
    fetchDishDetails() {
      const dishId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/dishes/${dishId}/`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.dish = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = 'Failed to fetch dish details';
            console.error('Error fetching dish details:', error);
          });
    },
    fetchPriceHistory() {
      const dishId = this.$route.params.id;
      fetch(`http://127.0.0.1:8000/api/dishes/price_history/${dishId}/`)
          .then(response => response.json())
          .then(data => {
            this.priceHistory = data;
          })
          .catch(error => {
            console.error('Error fetching price history:', error);
          });
    }
  }
};
</script>

<style scoped>
.details p {
  margin-bottom: 10px;
}
img {
  width: 100%; /* Adjust as needed */
  max-width: 400px; /* Adjust as needed */
  height: auto;
  display: block;
  margin: 0 auto;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  background: #f9f9f9;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
  width: 300px; /* 设置每个历史记录显示框的宽度 */
}
</style>