import { getAuth, reauthenticateWithPopup } from "firebase/auth";
import { getProvider } from "./provider-utils";

const deleteUser = async () => {
  const auth = getAuth();
  const user = auth.currentUser;
  const provider = getProvider();

  // 仮登録からメールリンクログインした場合、
  // IdP と未連携のままログインできる。
  if (!provider) {
    const result = confirm("退会しますか？");
    if (result) {
      await user.delete();
    }

    return;
  }

  try {
    // 退会する前に再認証。失敗するとエラーが発生。
    await reauthenticateWithPopup(user, provider);
    await user.delete();

    alert("退会しました。");
  } catch (error) {
    alert(`退会に失敗しました。\n${error.message}`);
  }
};

export default deleteUser;
