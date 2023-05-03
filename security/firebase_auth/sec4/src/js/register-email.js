import {
  getAuth,
  onAuthStateChanged,
  sendEmailVerification,
} from "firebase/auth";
import { initializeApp } from "firebase/app";
import firebaseConfig from "./firebase-config";
import logout from "./logout";

initializeApp(firebaseConfig);

const registerEmail = async (event) => {
  event.preventDefault();

  const emailForm = document.forms.emailForm.elements.email;
  const emailToRegistered = emailForm.value;

  const auth = getAuth();
  const user = auth.currentUser;
  auth.languageCode = "ja";

  const actionCodeSettings = {
    url: `https://${location.host}/login.html`,
  };

  if (user.email !== emailToRegistered) {
    try {
      await user.verifyBeforeUpdateEmail(emailToRegistered, actionCodeSettings);

      alert(`${emailToRegistered} に確認メールを送信しました。`);
      emailForm.value = "";
    } catch (error) {
      if (error.code === "auth/email-already-in-use") {
        const result = confirm(
          `${emailToRegistered} は既に登録されています。マイページにてこちらの SNS アカウントとの連携が可能です。別の SNS アカウントでログインしなおしますか？`
        );
        // 既存アカウトでログインし直す
        if (result) {
          // SNS アカウントの認証に成功している時点でユーザーが作られており、
          // このままでは既存アカウントに連携できなくなるので削除する
          await user.delete();
          window.location.href = "login.html";
          return;
        }

        emailForm.value = "";
        return;
      }
      alert(`Failed to send email\n${error.message}`);
    }
    return;
  }

  try {
    await sendEmailVerification(user);
    alert(`確認メールを ${emailToBeRegistered} に送信しました。`);
    emailForm.value = "";
  } catch (error) {
    alert(`Failed to send email\n${error.message}`);
  }
};

document.getElementById("emailForm").addEventListener("submit", registerEmail);

document.getElementById("logout").addEventListener("click", logout);

// loa
document.addEventListener("DOMContentLoaded", () => {
  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (!user) {
      window.location.href = "login.html";
      return;
    }

    const { email } = user;
    const emailForm = document.forms.emailForm.elements.email;
    emailForm.value = email;
  });
});
