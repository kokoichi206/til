import { GoogleAuthProvider, GithubAuthProvider, getAuth } from "firebase/auth";

export const getLinkedProviderIds = (user) => {
  return user.providerData
    .map((provider) => provider.providerId)
    .filter(
      (providerId) =>
        providerId === GoogleAuthProvider.PROVIDER_ID ||
        providerId === GithubAuthProvider.PROVIDER_ID
    );
};

export const getProvider = () => {
  const auth = getAuth();
  const providerIds = getLinkedProviderIds(auth.currentUser);

  let provider;
  // アプリとして, Google を優先する。
  if (providerIds.includes(GoogleAuthProvider.PROVIDER_ID)) {
    provider = new GoogleAuthProvider();
  } else if (providerIds.includes(GithubAuthProvider.PROVIDER_ID)) {
    provider = new GithubAuthProvider();
  }

  return provider;
};
