import { Outlet, NavLink, useLocation } from "react-router-dom";
import { useSyncStore } from "../store/syncStore";
import {
  Home,
  BookOpen,
  PenLine,
  Settings,
  RefreshCw,
  CloudOff,
  Cloud,
} from "lucide-react";

export default function Layout() {
  const { lastSync, isSyncing } = useSyncStore();
  const location = useLocation();
  const isOnline = navigator.onLine;

  const navItems = [
    { to: "/", icon: Home, label: "Dashboard" },
    { to: "/reading", icon: BookOpen, label: "Bible" },
    { to: "/journal", icon: PenLine, label: "Journal" },
    { to: "/settings", icon: Settings, label: "Settings" },
  ];

  return (
    <div className="flex h-screen bg-gray-900 text-white overflow-hidden">
      {/* Sidebar */}
      <aside className="w-16 flex flex-col items-center py-4 bg-gray-800 border-r border-gray-700">
        <div className="mb-8">
          <div className="w-10 h-10 bg-brand-500 rounded-lg flex items-center justify-center">
            <BookOpen size={20} />
          </div>
        </div>

        <nav className="flex-1 flex flex-col gap-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `p-3 rounded-lg transition-colors ${
                  isActive
                    ? "bg-brand-500/20 text-brand-400"
                    : "text-gray-400 hover:text-white hover:bg-gray-700"
                }`
              }
              title={item.label}
            >
              <item.icon size={20} />
            </NavLink>
          ))}
        </nav>

        {/* Sync status */}
        <div className="mt-auto mb-4">
          <button
            onClick={() => useSyncStore.getState().triggerSync()}
            disabled={isSyncing || !isOnline}
            className={`p-2 rounded-lg transition-colors ${
              isSyncing ? "animate-spin" : ""
            } ${
              isOnline
                ? "text-green-400 hover:bg-gray-700"
                : "text-gray-500 cursor-not-allowed"
            }`}
            title={
              isOnline
                ? lastSync
                  ? `Last sync: ${new Date(lastSync).toLocaleTimeString()}`
                  : "Click to sync"
                : "Offline"
            }
          >
            {isOnline ? (
              isSyncing ? (
                <RefreshCw size={18} />
              ) : (
                <Cloud size={18} />
              )
            ) : (
              <CloudOff size={18} />
            )}
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-auto">
        <div className="p-6 max-w-6xl mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
