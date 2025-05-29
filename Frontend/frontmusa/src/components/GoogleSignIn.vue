<template>
    <div>
      <!-- Automatisch gerendertes Button-Element -->
      <div class="g-signin2" data-onsuccess="onSignIn"></div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GoogleSignIn',
    mounted() {
      // Da wir den Callback global brauchen, hängen wir ihn ans Window
      window.onSignIn = this.onSignIn;
    },
    methods: {
      onSignIn(googleUser) {
        const profile = googleUser.getBasicProfile();
        console.log('ID Token:', googleUser.getAuthResponse().id_token);
        console.log('Name:', profile.getName());
        console.log('Email:', profile.getEmail());
        // TODO: ID Token an dein Backend senden, z.B. via fetch/axios
        this.$emit('signed-in', {
          idToken: googleUser.getAuthResponse().id_token,
          name: profile.getName(),
          email: profile.getEmail(),
          imageUrl: profile.getImageUrl(),
        });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Optional: zentrieren oder Größe anpassen */
  .g-signin2 {
    margin: 1rem auto;
  }
  </style>
  