<template>
  <div>
    <h2>Merchant Search</h2>
    <input type="text" v-model="query" placeholder="Enter search keyword">
    <button @click="searchMerchants">Search</button>

    <div v-if="loading">Loading...</div>

    <div v-if="!loading && merchants.length === 0">
      No results found.
    </div>

    <div v-if="merchants.length > 0">
      <h3>Search Results:</h3>
      <ul>
        <li v-for="merchant in merchants" :key="merchant.id">
          <router-link :to="{ name: 'MerchantDetail', params: { id: merchant.id } }">
            {{ merchant.name }} - {{ merchant.address }} - {{ merchant.phone }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      query: '',
      loading: false,
      merchants: [],
      error: null
    };
  },
  methods: {
    searchMerchants() {
      this.loading = true;
      fetch(`http://127.0.0.1:8000/api/merchants/search/?q=${this.query}`)
          .then(response => response.json())
          .then(data => {
            this.loading = false;
            this.merchants = data;
          })
          .catch(error => {
            this.loading = false;
            this.error = 'Failed to fetch search results';
            console.error('Error fetching search results:', error);
          });
    }
  }
};
</script>

<style scoped>
input {
  width: 200px;
  padding: 0.5rem;
  margin-right: 0.5rem;
}

button {
  padding: 0.5rem 1rem;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f9f9f9;
  width: 400px;
  margin: 0.5rem auto;
  padding: 0.5rem;
  border: 1px solid #ddd;
}

li a {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}
</style>

