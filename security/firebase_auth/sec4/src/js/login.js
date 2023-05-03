import {
  getAuth,
  signInWithPopup,
  GoogleAuthProvider,
  GithubAuthProvider,
} from "firebase/auth";
import { initializeApp } from "firebase/app";
import firebaseConfig from "./firebase-config";

initializeApp(firebaseConfig);

const redirectToMyPageWhenLoginSuccess = async (provider) => {
  try {
    const auth = getAuth();
    const result = await signInWithPopup(auth, provider);

    // when email is not verified
    if (!result.user.emailVerified) {
      window.location.href = "register-email.html";
      return;
    }

    window.location.href = "/";
  } catch (error) {
    // have logged in with github and tried to login with google
    if (error.code === "auth/account-exists-with-different-credential") {
      alert(
        `${error.customData.email} is already used with different provider`
      );
      return;
    }
    alert(`failed to login / sign up\n${error.message}`);
  }
};

const googleLogin = () => {
  redirectToMyPageWhenLoginSuccess(new GoogleAuthProvider());
};
document.getElementById("googleLogin").addEventListener("click", googleLogin);

const githubLogin = () => {
  redirectToMyPageWhenLoginSuccess(new GithubAuthProvider());
};
document.getElementById("githubLogin").addEventListener("click", githubLogin);
