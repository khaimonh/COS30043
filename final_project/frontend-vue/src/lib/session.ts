import { ref } from "vue";
import { api, getToken, loginRequest, setToken } from "./api";

export type SessionUser = {
  user_id: string;
  email: string;
  full_name: string;
  role: string;
};

export const token = ref<string | null>(getToken());
export const user = ref<SessionUser | null>(null);

export const isAdmin = () => user.value?.role === "Admin";

let mePromise: Promise<void> | null = null;

export async function fetchMe(): Promise<void> {
  if (!token.value) return;
  user.value = await api<SessionUser>("/auth/me");
}

export function ensureUser(): Promise<void> {
  if (user.value) return Promise.resolve();
  if (!token.value) return Promise.resolve();
  if (!mePromise) {
    mePromise = fetchMe().catch(() => {
      logout();
    });
  }
  return mePromise.finally(() => {
    mePromise = null;
  });
}

export async function login(email: string, password: string): Promise<void> {
  const accessToken = await loginRequest(email, password);
  setToken(accessToken);
  token.value = accessToken;
  await fetchMe();
}

export function logout(): void {
  setToken(null);
  token.value = null;
  user.value = null;
}
