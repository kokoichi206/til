import {
  getAuth,
  isSignInWithEmailLink,
  onAuthStateChanged,
} from "firebase/auth";
import logout from "./logout";
import { initializeApp } from "firebase/app";
import firebaseConfig from "./firebase-config";
import showLinkState from "./link-state";
import handleEmailSignIn from "./email-signin";
import updateEmail from "./update-email";
import deleteAccount from "./delete-user";

initializeApp(firebaseConfig);

document.getElementById("logout").addEventListener("click", logout);

document.getElementById("emailForm").addEventListener("submit", updateEmail);

document.getElementById("deleteAccount").addEventListener("click", deleteAccount);

document.addEventListener("DOMContentLoaded", async () => {
  const auth = getAuth();

  // メールリンクからのログインである場合。
  if (isSignInWithEmailLink(auth, window.location.href)) {
    await handleEmailSignIn();
  }

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

    showLinkState(user);
  });
});
