<template>
  <div class="expense-tracker">
    <h1>Отслеживание расходов</h1>

    <!-- Форма для добавления нового расхода -->
    <form @submit.prevent="addExpense" class="expense-form">
      <input
        v-model="newExpenseDescription"
        placeholder="Описание расхода"
        required
      />
      <input
        v-model.number="newExpenseAmount"
        type="number"
        step="0.01"
        placeholder="Сумма"
        required
      />
      <button type="submit">Добавить расход</button>
    </form>

    <!-- Список расходов -->
    <ul class="expense-list">
      <li v-for="expense in expenses" :key="expense.id" class="expense-item">
        <span>{{ expense.description }}</span>
        <span>{{ expense.amount }}</span>
        <button @click="deleteExpense(expense.id)" class="delete-button">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ExpenseTracker',
  data() {
    return {
      expenses: [],
      newExpenseDescription: '',
      newExpenseAmount: null,
    };
  },
  created() {
    this.fetchExpenses();
  },
  methods: {
    async fetchExpenses() {
      try {
        const response = await axios.get('http://localhost:8000/expenses/');
        this.expenses = response.data;
      } catch (error) {
        console.error('Ошибка при получении расходов:', error);
      }
    },
    async addExpense() {
      try {
        const newExpense = {
          description: this.newExpenseDescription,
          amount: parseFloat(this.newExpenseAmount),
        };
        await axios.post('http://localhost:8000/expenses/', newExpense);
        this.newExpenseDescription = '';
        this.newExpenseAmount = null;
        this.fetchExpenses(); // Обновляем список расходов
      } catch (error) {
        console.error('Ошибка при добавлении расхода:', error);
      }
    },
    async deleteExpense(id) {
      try {
        await axios.delete(`http://localhost:8000/expenses/${id}`);
        this.fetchExpenses(); // Обновляем список расходов
      } catch (error) {
        console.error('Ошибка при удалении расхода:', error);
      }
    },
  },
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
