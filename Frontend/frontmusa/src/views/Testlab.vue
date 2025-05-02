<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <h1>Hello HelloWorld</h1>
    <Register />
    <bookAppointment />
    <UserList />
  </div>
</template>

<script>
// @ is an alias to /src
import Register from "@/components/Register";
import bookAppointment from "@/components/bookAppointment";
import UserList from "@/components/UserList";

export default {
  name: "HomeView",
  components: {
    Register,
    bookAppointment,
    UserList,
  },
};
</script>