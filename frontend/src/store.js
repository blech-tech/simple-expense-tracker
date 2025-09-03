// src/store.js

import { ref } from 'vue';

export const isAuthenticated = ref(!!localStorage.getItem('token'));