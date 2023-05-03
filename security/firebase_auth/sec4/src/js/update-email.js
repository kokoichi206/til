import {
  getAuth,
  reauthenticateWithPopup,
  verifyBeforeUpdateEmail,
} from "firebase/auth";
import { getProvider } from "./provider-utils";

const updateEmail = async (event) => {
  event.preventDefault();

  const emailForm = document.forms.emailForm.elements.email;
  const email = emailForm.value;

  const actionCodeSettings = {
    url: `https://${location.host}/login.html`,
  };

  const auth = getAuth();
  auth.languageCode = "ja";

  const user = auth.currentUser;

  if (user.email === email) {
    alert("現在のメールアドレスと同じです。");
    return;
  }

  const provider = getProvider();

  try {
    // メールアドレスを更新する前に再認証。失敗するとエラーが起きる。
    await reauthenticateWithPopup(user, provider);
    await verifyBeforeUpdateEmail(user, email, actionCodeSettings);
    alert(`${email} に確認メールを送信しました。`);
    emailForm.value = "";
  } catch (error) {
    if (error.code === "auth/email-already-in-use") {
      alert(`${email} に確認メールを送信しました。`);
      emailForm.value = "";

      return;
    }

    alert(`メールの送信に失敗しました。\n${error.message}`);
  }
};

export default updateEmail;
