import { getAuth } from "firebase/auth";

const logout = async () => {
  const auth = getAuth();
  auth.signOut();
};

export default logout;
