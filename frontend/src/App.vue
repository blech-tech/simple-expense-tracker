<template>
  <div class="app-container">
    <header v-if="isAuthenticated" class="app-header">
      <button class="btn btn-danger" @click="handleLogout">Выйти</button>
    </header>

    <main v-if="isAuthenticated">
      <ExpenseTracker />
    </main>

    <main v-else>
      <Login v-if="currentView === 'login'" @login-success="handleLogin" @switch-to-register="currentView = 'register'" />
      <Register v-if="currentView === 'register'" @switch-to-login="currentView = 'login'" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ExpenseTracker from './components/ExpenseTracker.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';

const isAuthenticated = ref(false);
const currentView = ref('login');

const handleLogin = () => {
  isAuthenticated.value = true;
};

const handleLogout = () => {
  localStorage.removeItem('token');
  isAuthenticated.value = false;
  currentView.value = 'login';
};

onMounted(() => {
  const token = localStorage.getItem('token');
  if (token) {
    isAuthenticated.value = true;
  }
});
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