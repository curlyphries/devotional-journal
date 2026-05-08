import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { invoke } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";

import { useAuthStore } from "./store/authStore";
import { useSyncStore } from "./store/syncStore";

import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import JournalEditor from "./pages/JournalEditor";
import Reader from "./pages/Reader";
import Settings from "./pages/Settings";
import Login from "./pages/Login";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  const { isAuthenticated, checkAuth } = useAuthStore();
  const { triggerSync } = useSyncStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check auth status on startup
    checkAuth().finally(() => setIsLoading(false));

    // Listen for tray sync trigger
    const unlisten = listen("trigger-sync", () => {
      triggerSync();
    });

    // Periodic sync when online
    const syncInterval = setInterval(() => {
      if (navigator.onLine) {
        triggerSync();
      }
    }, 30000); // Every 30 seconds

    return () => {
      unlisten.then((f) => f());
      clearInterval(syncInterval);
    };
  }, [checkAuth, triggerSync]);

  if (isLoading) {
    return (
      <div className="h-screen w-full flex items-center justify-center bg-gray-900 text-white">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/login"
            element={isAuthenticated ? <Navigate to="/" /> : <Login />}
          />
          <Route
            path="/"
            element={isAuthenticated ? <Layout /> : <Navigate to="/login" />}
          >
            <Route index element={<Dashboard />} />
            <Route path="journal" element={<JournalEditor />} />
            <Route path="journal/:id" element={<JournalEditor />} />
            <Route path="reading" element={<Reader />} />
            <Route path="settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
