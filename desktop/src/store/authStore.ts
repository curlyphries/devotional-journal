import { create } from "zustand";
import { invoke } from "@tauri-apps/api/core";

interface AuthState {
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  login: (email: string, apiUrl: string) => Promise<void>;
  verifyMagicLink: (token: string) => Promise<void>;
  checkAuth: () => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  isLoading: false,
  error: null,

  login: async (email, apiUrl) => {
    set({ isLoading: true, error: null });
    try {
      await invoke("authenticate", { email, apiUrl });
      set({ isLoading: false });
    } catch (err) {
      set({ error: String(err), isLoading: false });
      throw err;
    }
  },

  verifyMagicLink: async (token) => {
    set({ isLoading: true, error: null });
    try {
      await invoke("verify_magic_link", { token });
      set({ isAuthenticated: true, isLoading: false });
    } catch (err) {
      set({ error: String(err), isLoading: false });
      throw err;
    }
  },

  checkAuth: async () => {
    try {
      const status = await invoke<{
        configured: boolean;
        authenticated: boolean;
      }>("get_sync_status");
      set({ isAuthenticated: status.authenticated });
    } catch {
      set({ isAuthenticated: false });
    }
  },

  logout: async () => {
    // Clear local data
    set({ isAuthenticated: false, error: null });
  },
}));
