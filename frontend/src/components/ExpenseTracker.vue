<template>
  <div class="expense-tracker">
    <h1>Отслеживание расходов</h1>
    <p v-if="message">{{ message }}</p>

    <form @submit.prevent="editingExpense ? updateExpense() : addExpense()" class="expense-form">
      <input
        v-model="computedDescription"
        placeholder="Описание расхода"
        required
      />
      <input
        v-model.number="computedAmount"
        type="number"
        step="0.01"
        placeholder="Сумма"
        required
      />
      <button type="submit">{{ editingExpense ? 'Сохранить изменения' : 'Добавить расход' }}</button>
      <button v-if="editingExpense" @click="cancelEditing" type="button">Отмена</button>
    </form>

    <ul class="expense-list">
      <li v-for="expense in expenses" :key="expense.id" class="expense-item">
        <span>{{ expense.description }}</span>
        <span>{{ expense.amount }}</span>
        <button @click="startEditing(expense)" class="edit-button">Редактировать</button>
        <button @click="deleteExpense(expense.id)" class="delete-button">Удалить</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const expenses = ref([]);
const description = ref('');
const amount = ref('');
const message = ref('');
const editingExpense = ref(null);

const computedDescription = computed({
  get: () => editingExpense.value ? editingExpense.value.description : description.value,
  set: (value) => {
    if (editingExpense.value) {
      editingExpense.value.description = value;
    } else {
      description.value = value;
    }
  }
});

const computedAmount = computed({
  get: () => editingExpense.value ? editingExpense.value.amount : amount.value,
  set: (value) => {
    if (editingExpense.value) {
      editingExpense.value.amount = value;
    } else {
      amount.value = value;
    }
  }
});

const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  if (token) {
    return {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
  }
  return {};
};

const fetchExpenses = async () => {
  try {
    const response = await axios.get('http://localhost:8000/expenses/', getAuthHeaders());
    expenses.value = response.data;
  } catch (error) {
    message.value = 'Ошибка загрузки расходов. Пожалуйста, войдите в систему.';
  }
};

const addExpense = async () => {
  try {
    const newExpense = {
      description: description.value,
      amount: parseFloat(amount.value)
    };
    await axios.post('http://localhost:8000/expenses/', newExpense, getAuthHeaders());
    message.value = 'Расход успешно добавлен!';
    description.value = '';
    amount.value = '';
    await fetchExpenses();
  } catch (error) {
    message.value = 'Не удалось добавить расход. Пожалуйста, войдите в систему.';
  }
};

const deleteExpense = async (id) => {
  try {
    await axios.delete(`http://localhost:8000/expenses/${id}`, getAuthHeaders());
    message.value = 'Расход успешно удален!';
    await fetchExpenses();
  } catch (error) {
    message.value = 'Ошибка при удалении расхода. Возможно, у вас нет прав.';
  }
};

const startEditing = (expense) => {
  editingExpense.value = { ...expense };
};

const updateExpense = async () => {
  try {
    const updatedExpense = {
      description: editingExpense.value.description,
      amount: parseFloat(editingExpense.value.amount)
    };
    await axios.put(`http://localhost:8000/expenses/${editingExpense.value.id}`, updatedExpense, getAuthHeaders());
    message.value = 'Расход успешно обновлен!';
    editingExpense.value = null;
    await fetchExpenses();
  } catch (error) {
    message.value = 'Не удалось обновить расход. Возможно, у вас нет прав.';
  }
};

const cancelEditing = () => {
  editingExpense.value = null;
};

onMounted(() => {
  fetchExpenses();
});

defineExpose({
  fetchExpenses
});
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

.edit-button {
  background-color: #3f7de9;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #3461a3;
}
</style>