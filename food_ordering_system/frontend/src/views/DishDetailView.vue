<template>
  <div>
    <UserLogoutButton />
    <h1>Dish Details</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Name: {{ dish.name }}</p>
      <p>price: {{ dish.price }}</p>
      <p><img :src="dish.image_url" alt="Dish Image"></p>
      <!-- Add more details here as needed -->
    </div>
  </div>
</template>

<script>
import UserLogoutButton from "@/components/UserLogoutButton.vue";

export default {
  components: {UserLogoutButton},
  data() {
    return {
      loading: true,
      dish: null,
      error: null
    };
  },
  mounted() {
    this.fetchDishDetails();
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
    }
  }
};
</script>

<style>

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
</style>
