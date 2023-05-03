import {
  GoogleAuthProvider,
  GithubAuthProvider,
  linkWithPopup,
  unlink,
} from "firebase/auth";
import { getLinkedProviderIds } from "./provider-utils";

const linkProvider = async (user, provider) => {
  try {
    await linkWithPopup(user, provider);
    window.location.reload();
  } catch (error) {
    alert(`failed to link: ${error.message}`);
  }
};

// IdP 連携解除ボタン
const unlinkProvider = async (user, provider) => {
  try {
    await unlink(user, provider.providerId);
    alert(`${provider} との連携を解除しました。`);
    window.location.reload();
  } catch (error) {
    alert(`failed to unlink: ${error.message}`);
  }
};

const getProviderDisplayName = (user, providerId) => {
  return user.providerData.find(
    (provider) => provider.providerId === providerId
  ).displayName;
};

// 連携済み IdP のユーザー情報のセット
const setLinkedProvider = (user, info) => {
  const providerId = info.provider.providerId;
  const providerDisplayName = getProviderDisplayName(user, providerId);

  info.linkState.textContent = "連携済み";
  info.displayName.textContent = providerDisplayName;
  info.button.textContent = "解除";

  info.button.addEventListener("click", () => {
    unlinkProvider(user, info.provider);
  });
};

// 未連携の IdP のユーザー情報のセット
const setNotLinkedProvider = (user, info) => {
  info.linkState.textContent = "未連携";
  info.displayName.textContent = "-";
  info.button.textContent = "連携";

  info.button.addEventListener("click", () => {
    linkProvider(user, info.provider);
  });
};

const showLinkState = (user) => {
  console.log("showLinkState");

  const linkedProviderIds = getLinkedProviderIds(user);

  const linkInfos = [
    {
      provider: new GoogleAuthProvider(),
      linkState: document.getElementById("googleLinkState"),
      displayName: document.getElementById("googleDisplayName"),
      button: document.getElementById("googleLinkButton"),
    },
    {
      provider: new GithubAuthProvider(),
      linkState: document.getElementById("githubLinkState"),
      displayName: document.getElementById("githubDisplayName"),
      button: document.getElementById("githubLinkButton"),
    },
  ];

  linkInfos.forEach((info) => {
    if (!linkedProviderIds.includes(info.provider.providerId)) {
      setNotLinkedProvider(user, info);
      return;
    }

    setLinkedProvider(user, info);
  });

  // どちらか一方しか連携していない場合は、解除ボタンを非表示にする。
  // （何か1つはログイン手段を残しておかせる）
  if (
    linkedProviderIds.includes(GoogleAuthProvider.PROVIDER_ID) &&
    !linkedProviderIds.includes(GithubAuthProvider.PROVIDER_ID)
  ) {
    document.getElementById("googleLinkButton").style.display = "none";
  } else if (
    !linkedProviderIds.includes(GoogleAuthProvider.PROVIDER_ID) &&
    linkedProviderIds.includes(GithubAuthProvider.PROVIDER_ID)
  ) {
    document.getElementById("githubLinkButton").style.display = "none";
  }
};

export default showLinkState;
