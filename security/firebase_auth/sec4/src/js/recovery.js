import {
  getAuth,
  onAuthStateChanged,
  fetchSignInMethodsForEmail,
  sendSignInLinkToEmail,
} from "firebase/auth";
import { initializeApp } from "firebase/app";
import firebaseConfig from "./firebase-config";

initializeApp(firebaseConfig);

const sendLoginLink = async (event) => {
  event.preventDefault();

  const emailForm = document.forms.emailForm.elements.email;
  const email = emailForm.value;

  const actionCodeSettings = {
    url: `https://${location.host}`,
    handleCodeInApp: true, // true if you wanna send login URL
  };

  const auth = getAuth();
  auth.languageCode = "ja";

  try {
    const signInMethods = await fetchSignInMethodsForEmail(auth, email);

    // 未登録の場合
    if (signInMethods.length === 0) {
      emailForm.value = "";
      alert(`${email} が登録済みの場合、ログイン用の URL が送られています。`);
      return;
    }

    await sendSignInLinkToEmail(auth, email, actionCodeSettings);
    emailForm.value = "";
    alert(`${email} が登録済みの場合、ログイン用の URL が送られています。`);
    return;
  } catch (error) {
    alert(`Failed to send email\n${error.message}`);
  }
};

document.getElementById("emailForm").addEventListener("submit", sendLoginLink);

document.addEventListener("DOMContentLoaded", () => {
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (!user) {
      return;
    }

    window.location.href = "/";
  });
});
