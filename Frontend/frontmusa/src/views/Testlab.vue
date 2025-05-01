<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <HelloWorld msg="Welcome to Your Vue.js App" />
    <Register />
    <bookAppointment />
    <UserList />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";
import Register from "@/components/Register";
import bookAppointment from "@/components/bookAppointment";
import UserList from "@/components/UserList";

export default {
  name: "HomeView",
  components: {
    HelloWorld,
    Register,
    bookAppointment,
    UserList,
  },
};
</script>
