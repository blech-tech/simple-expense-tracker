// src/App.vue

<template>
  <div class="app-container">
    <header v-if="isAuthenticated" class="app-header">
      <button class="btn btn-danger" @click="handleLogout">Выйти</button>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { isAuthenticated } from './store'; // Import the global state

const router = useRouter();

const handleLogout = () => {
  localStorage.removeItem('token');
  isAuthenticated.value = false; // Update the global state
  router.push({ name: 'Login' });
};
</script>

<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.app-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}
</style>