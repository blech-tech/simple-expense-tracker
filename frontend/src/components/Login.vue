<template>
    <div class="expense-tracker">
      <h1>Вход</h1>
      <form @submit.prevent="handleLogin" class="expense-form">
        <div>
          <label>Имя пользователя</label>
          <input
            type="text"
            v-model="username"
            required
          />
        </div>
        <div>
          <label>Пароль</label>
          <input
            type="password"
            v-model="password"
            required
          />
        </div>
        <button type="submit">Войти</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p>
        Нет аккаунта?
        <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </template>
  

  <script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { isAuthenticated } from '../store'; // Import the global state

const username = ref('');
const password = ref('');
const message = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost/api/token', new URLSearchParams({
      username: username.value,
      password: password.value,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    localStorage.setItem('token', response.data.access_token);
    isAuthenticated.value = true; // Update the global state
    message.value = 'Вход выполнен успешно!';
    router.push({ name: 'ExpenseTracker' });
  } catch (error) {
    message.value = 'Не удалось войти. Неверные данные.';
  }
};
</script>
  
  <style scoped>
  /* Ваши текущие стили */
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
    flex-direction: column; /* Изменили на column для лучшего расположения */
    gap: 15px; /* Увеличили отступы */
    margin-bottom: 20px;
  }
  
  .expense-form input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 100%; /* Убрали flex-grow и сделали ширину 100% */
    box-sizing: border-box; /* Важное свойство, чтобы padding не увеличивал ширину */
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
  </style>