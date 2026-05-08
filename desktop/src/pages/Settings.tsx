import { useAuthStore } from "../store/authStore";
import { useSyncStore } from "../store/syncStore";
import { invoke } from "@tauri-apps/api/core";
import {
  User,
  Cloud,
  Shield,
  Bell,
  Palette,
  LogOut,
  RefreshCw,
} from "lucide-react";

export default function Settings() {
  const { isAuthenticated, logout } = useAuthStore();
  const { lastSync, isSyncing, triggerSync } = useSyncStore();

  const handleClearData = async () => {
    if (
      confirm(
        "This will delete all local data and sign you out. Are you sure?"
      )
    ) {
      await invoke("wipe_keys");
      await logout();
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">Settings</h1>

      <div className="space-y-6">
        {/* Account */}
        <section className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <User size={20} className="text-brand-400" />
            <h2 className="text-lg font-semibold">Account</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between py-2 border-b border-gray-700">
              <span className="text-gray-400">Status</span>
              <span
                className={
                  isAuthenticated ? "text-green-400" : "text-yellow-400"
                }
              >
                {isAuthenticated ? "Signed In" : "Not signed in"}
              </span>
            </div>

            <button
              onClick={handleClearData}
              className="w-full py-2 text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
            >
              Sign Out & Clear Data
            </button>
          </div>
        </section>

        {/* Sync */}
        <section className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Cloud size={20} className="text-brand-400" />
              <h2 className="text-lg font-semibold">Sync</h2>
            </div>
            <button
              onClick={triggerSync}
              disabled={isSyncing}
              className="flex items-center gap-2 px-3 py-1 bg-brand-600 hover:bg-brand-500 rounded-lg text-sm disabled:opacity-50"
            >
              <RefreshCw size={16} className={isSyncing ? "animate-spin" : ""} />
              Sync Now
            </button>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between py-2 border-b border-gray-700">
              <span className="text-gray-400">Last Sync</span>
              <span className="text-sm">
                {lastSync
                  ? new Date(lastSync).toLocaleString()
                  : "Never"}
              </span>
            </div>

            <div className="flex items-center justify-between py-2 border-b border-gray-700">
              <span className="text-gray-400">Auto Sync</span>
              <span className="text-green-400 text-sm">Enabled (30s)</span>
            </div>
          </div>
        </section>

        {/* Security */}
        <section className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <Shield size={20} className="text-brand-400" />
            <h2 className="text-lg font-semibold">Security</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">App Lock</p>
                <p className="text-sm text-gray-400">
                  Require authentication to open
                </p>
              </div>
              <button className="relative w-12 h-6 bg-gray-600 rounded-full transition-colors">
                <span className="absolute left-1 top-1 w-4 h-4 bg-white rounded-full transition-transform" />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Auto-Lock</p>
                <p className="text-sm text-gray-400">
                  Lock after 5 minutes of inactivity
                </p>
              </div>
              <button className="relative w-12 h-6 bg-brand-600 rounded-full transition-colors">
                <span className="absolute right-1 top-1 w-4 h-4 bg-white rounded-full" />
              </button>
            </div>
          </div>
        </section>

        {/* Appearance */}
        <section className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <Palette size={20} className="text-brand-400" />
            <h2 className="text-lg font-semibold">Appearance</h2>
          </div>

          <div className="flex items-center justify-between py-2">
            <span className="text-gray-400">Theme</span>
            <select className="bg-gray-700 rounded-lg px-3 py-1 text-sm">
              <option>System</option>
              <option>Dark</option>
              <option>Light</option>
            </select>
          </div>
        </section>

        {/* Notifications */}
        <section className="bg-gray-800 rounded-lg p-6">
          <div className="flex items-center gap-3 mb-4">
            <Bell size={20} className="text-brand-400" />
            <h2 className="text-lg font-semibold">Notifications</h2>
          </div>

          <div className="space-y-3">
            <label className="flex items-center justify-between cursor-pointer">
              <span>Daily Reminder</span>
              <input type="checkbox" defaultChecked className="w-4 h-4" />
            </label>
            <label className="flex items-center justify-between cursor-pointer">
              <span>Streak Alerts</span>
              <input type="checkbox" defaultChecked className="w-4 h-4" />
            </label>
          </div>
        </section>

        {/* About */}
        <section className="bg-gray-800 rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4">About</h2>
          <div className="space-y-2 text-sm text-gray-400">
            <p>Devotional Journal Desktop v0.1.0</p>
            <p>Built with Tauri + React</p>
            <p>© 2026 curlyphries</p>
          </div>
        </section>
      </div>
    </div>
  );
}
