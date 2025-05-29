// src/plugins/googleAuth.js
let auth2 = null;

export function loadGoogleAuth() {
  return new Promise((resolve, reject) => {
    // Wenn schon geladen, resolve sofort
    if (auth2) {
      return resolve(auth2);
    }

    // Warte, bis gapi geladen ist
    window.gapi.load('auth2', () => {
      // Initialisiere mit deiner Client-ID
      window.gapi.auth2
        .init({
          client_id: document
            .querySelector('meta[name="google-signin-client_id"]')
            .getAttribute('content'),
        })
        .then((googleAuth) => {
          auth2 = googleAuth;
          resolve(auth2);
        })
        .catch(reject);
    });
  });
}

export function signOutGoogle() {
    if (!auth2) {
      return Promise.reject(new Error('Google Auth noch nicht initialisiert'));
    }
    return auth2.signOut().then(() => {
      console.log('User signed out.');
    });
  }
  