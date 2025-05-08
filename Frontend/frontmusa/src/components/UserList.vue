<template>
  <div class="userlist-container">
    <div class="userlist-card">
      <h2>Benutzerliste</h2>
      <div class="user-list">
        <div v-for="user in users" :key="user.id" class="user-item">
          <div class="user-info">
            <span class="user-name">{{ user.name }}</span>
            <span class="user-email">{{ user.email }}</span>
            <span class="user-phone">{{ user.phonenumber }}</span>
            <span class="user-role" :class="user.role">{{ user.role }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import axios from "axios";
import { API_ENDPOINTS } from "../config";

export default {
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get(API_ENDPOINTS.USERS);
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>
  
<style scoped>
.userlist-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  padding: 2rem;
  background-color: #f5f5f5;
}

.userlist-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 800px;
}

h2 {
  color: #333;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.user-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
  align-items: center;
}

.user-name {
  font-weight: bold;
  color: #333;
}

.user-email {
  color: #666;
}

.user-phone {
  color: #666;
}

.user-role {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  text-align: center;
  text-transform: capitalize;
}

.user-role.kunde {
  background-color: #e3f2fd;
  color: #1976d2;
}

.user-role.admin {
  background-color: #fce4ec;
  color: #c2185b;
}

@media (max-width: 768px) {
  .userlist-card {
    padding: 1.5rem;
  }

  .user-info {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
  