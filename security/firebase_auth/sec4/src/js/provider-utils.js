import { GoogleAuthProvider, GithubAuthProvider } from "firebase/auth";

export const getLinkedProviderIds = (user) => {
  return user.providerData
    .map((provider) => provider.providerId)
    .filter(
      (providerId) =>
        providerId === GoogleAuthProvider.PROVIDER_ID ||
        providerId === GithubAuthProvider.PROVIDER_ID
    );
};
