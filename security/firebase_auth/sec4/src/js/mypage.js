import {
  getAuth,
  isSignInWithEmailLink,
  onAuthStateChanged,
} from "firebase/auth";
import logout from "./logout";
import { initializeApp } from "firebase/app";
import firebaseConfig from "./firebase-config";

initializeApp(firebaseConfig);

document.getElementById("logout").addEventListener("click", logout);

document.addEventListener("DOMContentLoaded", async () => {
  const auth = getAuth();

  onAuthStateChanged(auth, (user) => {
    if (!user) {
      window.location.href = "login.html";
      return;
    }

    if (!user.emailVerified) {
      window.location.href = "register-email.html";
      return;
    }

    const { email, displayName } = user;

    document.getElementById(
      "top-message"
    ).textContent = `${displayName} さん、こんにちは！`;

    document.getElementById("currentEmail").textContent = email;
  });
});
