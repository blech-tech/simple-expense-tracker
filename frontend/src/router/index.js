// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ExpenseTracker from '../components/ExpenseTracker.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: { title: 'Login • Expense Tracker' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: 'Register • Expense Tracker' }
  },
  {
    path: '/expenses',
    name: 'ExpenseTracker',
    component: ExpenseTracker,
    meta: { requiresAuth: true, title: 'My Expenses • Expense Tracker' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login' });
  } else {
    next();
  }
});

router.afterEach((to) => {
  const defaultTitle = 'Expense Tracker';
  document.title = to.meta?.title || defaultTitle;
});

export default router;