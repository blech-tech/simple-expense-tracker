<template>
    <div class="expense-tracker">
      <h1>Регистрация</h1>
      <form @submit.prevent="handleRegister" class="expense-form">
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
        <button type="submit">Зарегистрироваться</button>
      </form>
      <p v-if="message">{{ message }}</p>
      <p>
        Уже есть аккаунт?
        <router-link to="/">Войти</router-link>
      </p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router'; // <-- Добавляем import useRouter
  
  const username = ref('');
  const password = ref('');
  const message = ref('');
  
  const router = useRouter(); // <-- Инициализируем роутер
  
  const handleRegister = async () => {
    try {
      await axios.post('http://localhost:8000/users/', {
        username: username.value,
        password: password.value,
      });
      message.value = 'Регистрация успешна! Теперь вы можете войти.';
      router.push({ name: 'Login' }); // <-- Навигация на страницу входа
  
    } catch (error) {
      message.value = 'Не удалось зарегистрироваться. Пользователь уже существует?';
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
    flex-direction: column;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .expense-form input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 100%;
    box-sizing: border-box;
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