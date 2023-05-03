import { getAuth, signInWithEmailLink } from "firebase/auth";
import { getLinkedProviderIds } from "./provider-utils";

const handleEmailSignIn = async () => {
  const auth = getAuth();
  const email = window.prompt("確認のためのメールアドレスを入力してください。");

  try {
    const result = await signInWithEmailLink(auth, email, window.location.href);
    const linkedProviderIds = getLinkedProviderIds(result.user);

    // 仮登録中のメールアドレスでメールリンクログインをすると、
    // Firebase Auth の仕様で IdP の連携が解除される！
    if (linkedProviderIds.length === 0) {
      alert("メールが使えない場合に備えて、\nIdP との連携をお願いします。");
    }
  } catch (error) {
    alert(`failed to login: ${error.message}`);
  }
};

export default handleEmailSignIn;
