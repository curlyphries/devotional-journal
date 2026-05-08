import { useState } from "react";
import { useAuthStore } from "../store/authStore";
import { BookOpen, Loader2 } from "lucide-react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [apiUrl, setApiUrl] = useState("http://localhost:8001");
  const [magicLinkSent, setMagicLinkSent] = useState(false);
  const { login, verifyMagicLink, isLoading, error } = useAuthStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, apiUrl);
      setMagicLinkSent(true);
    } catch {
      // Error is stored in state
    }
  };

  const handleVerify = async (token: string) => {
    try {
      await verifyMagicLink(token);
    } catch {
      // Error is stored in state
    }
  };

  // Auto-detect token from URL (for magic link callback)
  if (!magicLinkSent) {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    if (token) {
      handleVerify(token);
      return (
        <div className="h-screen flex items-center justify-center bg-gray-900 text-white">
          <Loader2 className="animate-spin" size={32} />
        </div>
      );
    }
  }

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-4">
      <div className="w-full max-w-md">
        <div className="flex items-center justify-center mb-8">
          <div className="w-12 h-12 bg-brand-500 rounded-xl flex items-center justify-center mr-3">
            <BookOpen size={24} />
          </div>
          <h1 className="text-2xl font-bold">Devotional Journal</h1>
        </div>

        {magicLinkSent ? (
          <div className="bg-gray-800 rounded-lg p-6 text-center">
            <h2 className="text-xl font-semibold mb-4">Check your email</h2>
            <p className="text-gray-400 mb-4">
              We&apos;ve sent a magic link to {email}. Click it to sign in.
            </p>
            <button
              onClick={() => setMagicLinkSent(false)}
              className="text-brand-400 hover:text-brand-300"
            >
              Use a different email
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Sign In</h2>

            {error && (
              <div className="bg-red-500/20 text-red-400 p-3 rounded mb-4 text-sm">
                {error}
              </div>
            )}

            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="w-full px-3 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-brand-500 focus:outline-none"
                placeholder="you@example.com"
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium mb-2">
                API Server URL
              </label>
              <input
                type="url"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                required
                className="w-full px-3 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:border-brand-500 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2 bg-brand-600 hover:bg-brand-500 rounded-lg font-medium disabled:opacity-50 flex items-center justify-center"
            >
              {isLoading ? (
                <Loader2 className="animate-spin" size={20} />
              ) : (
                "Send Magic Link"
              )}
            </button>

            <p className="mt-4 text-sm text-gray-400 text-center">
              No password needed. Secure magic link authentication.
            </p>
          </form>
        )}
      </div>
    </div>
  );
}
