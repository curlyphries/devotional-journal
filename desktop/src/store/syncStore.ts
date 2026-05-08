import { create } from "zustand";
import { invoke } from "@tauri-apps/api/core";

interface SyncState {
  lastSync: string | null;
  isSyncing: boolean;
  pendingCount: number;
  error: string | null;
  
  // Actions
  triggerSync: () => Promise<void>;
  getStatus: () => Promise<void>;
}

export const useSyncStore = create<SyncState>((set, get) => ({
  lastSync: null,
  isSyncing: false,
  pendingCount: 0,
  error: null,

  triggerSync: async () => {
    if (get().isSyncing) return;
    
    set({ isSyncing: true, error: null });
    try {
      const result = await invoke<{
        success: boolean;
        server_changes_count: number;
        pending_cleared: number;
      }>("trigger_sync");
      
      set({
        lastSync: new Date().toISOString(),
        isSyncing: false,
        pendingCount: Math.max(0, get().pendingCount - result.pending_cleared),
      });
    } catch (err) {
      set({ error: String(err), isSyncing: false });
    }
  },

  getStatus: async () => {
    try {
      const status = await invoke<{
        last_sync?: string;
      }>("get_sync_status");
      set({ lastSync: status.last_sync || null });
    } catch (err) {
      console.error("Failed to get sync status:", err);
    }
  },
}));
