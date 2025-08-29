<template>
    <div class="expense-tracker"> <div class="container">
        <h2>Вход</h2>
        <form @submit.prevent="handleLogin" class="expense-form"> <div class="form-group">
            <label>Имя пользователя</label>
            <input
              type="text"
              class="form-control"
              v-model="username"
              required
            />
          </div>
          <div class="form-group">
            <label>Пароль</label>
            <input
              type="password"
              class="form-control"
              v-model="password"
              required
            />
          </div>
          <button type="submit">Войти</button> </form>
        <p v-if="message">{{ message }}</p>
        <p>
          Нет аккаунта?
          <button class="btn btn-link" @click="$emit('switch-to-register')">Зарегистрироваться</button>
        </p>
      </div>
    </div>
  </template>

  
  <script setup>
  import { ref, defineEmits } from 'vue';
  import axios from 'axios';
  
  const emit = defineEmits(['login-success', 'switch-to-register']);
  
  const username = ref('');
  const password = ref('');
  const message = ref('');
  
  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:8000/token', 
        new URLSearchParams({
          username: username.value,
          password: password.value,
        })
      );
      const token = response.data.access_token;
      localStorage.setItem('token', token);
      emit('login-success');
    } catch (error) {
      message.value = 'Неверное имя пользователя или пароль.';
    }
  };
  </script>

<style scoped>
.expense-tracker {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
}

.expense-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.expense-form input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.expense-form button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.expense-form button:hover {
  background-color: #45a049;
}

.expense-list {
  list-style: none;
  padding: 0;
}

.expense-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.expense-item:last-child {
  border-bottom: none;
}

.expense-item span {
  flex-grow: 1;
}

.delete-button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #da190b;
}
</style>