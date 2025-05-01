// auth.js
import { reactive } from "vue";

export const auth = reactive({
    token: localStorage.getItem("access_token") || null,
    user: {} // initial leer, später z. B. { name: "Max" }
});

export function setToken(token, userData = {}) {
    auth.token = token;
    auth.user = userData; // hier wird der gesamte Benutzer-Objekt gespeichert
    localStorage.setItem("access_token", token);
    // Optional: lokale Speicherung von userData, wenn benötigt
}

export function clearToken() {
    auth.token = null;
    auth.user = {};
    localStorage.removeItem("access_token");
    // Lösche ggf. gespeicherte User-Daten auch aus LocalStorage
}