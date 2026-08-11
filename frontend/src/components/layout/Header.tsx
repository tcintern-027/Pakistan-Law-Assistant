import { Moon, Scale } from "lucide-react";

function Header() {
  return (
    <header className="border-b border-white/10 bg-[#0f1420]/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600">
            <Scale size={20} />
          </div>

          <div>
            <h1 className="text-sm font-semibold">
              Pakistan Law Assistant
            </h1>

            <p className="text-xs text-gray-500">
              AI-powered legal information
            </p>
          </div>
        </div>

        <button
          type="button"
          className="flex h-9 w-9 items-center justify-center rounded-lg border border-white/10 text-gray-400 transition hover:bg-white/5 hover:text-white"
          aria-label="Toggle theme"
        >
          <Moon size={18} />
        </button>
      </div>
    </header>
  );
}

export default Header;