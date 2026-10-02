import React from 'react';
import { ArrowUp, ShieldCheck } from 'lucide-react';
import { sound } from '../utils/audio';

export const Footer: React.FC = () => {
  const scrollToTop = () => {
    sound.playClick(1100);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-white border-t-2 border-fintech-black pt-16 pb-12 text-fintech-black font-sans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Top Section: Brand + Columns */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 pb-16 border-b border-fintech-black/20">
          
          {/* Left 4 Cols: Brand & Tagline */}
          <div className="lg:col-span-4 space-y-4">
            {/* Boxed Logo */}
            <div className="inline-block p-1 border-2 border-fintech-black bg-white shadow-brutal-sm">
              <div className="border border-fintech-black px-4 py-2 flex items-center space-x-2">
                <div className="w-2.5 h-2.5 bg-fintech-blue border border-fintech-black"></div>
                <span className="font-display font-extrabold text-xl tracking-tight text-fintech-black">
                  LEGACY<span className="text-fintech-blue">AI</span>
                </span>
              </div>
            </div>

            {/* Exact Tagline */}
            <div className="font-display font-bold text-lg text-fintech-black tracking-tight uppercase leading-snug pt-2">
              INTELLIGENT FINANCE.<br />
              BUILT FOR WHAT'S NEXT.
            </div>

            <p className="text-xs text-fintech-muted font-sans max-w-sm leading-relaxed">
              An institutional-grade financial intelligence engine empowering individuals and enterprises to govern wealth with autonomous precision.
            </p>

            {/* Micro System Status Pill */}
            <div className="inline-flex items-center space-x-2 border border-fintech-black/30 bg-fintech-paper px-2.5 py-1 text-[11px] font-mono">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
              <span className="text-fintech-black font-semibold">CORE NETWORK: OPERATIONAL</span>
            </div>
          </div>

          {/* Right 8 Cols: 4 Columns */}
          <div className="lg:col-span-8 grid grid-cols-2 sm:grid-cols-4 gap-8 font-mono text-xs">
            
            {/* Column 1: PLATFORM */}
            <div className="space-y-3">
              <div className="font-extrabold text-fintech-black uppercase tracking-wider pb-1 border-b border-fintech-black/20">
                [PLATFORM]
              </div>
              <ul className="space-y-2.5 text-fintech-muted">
                {['AI Financial Advisor', 'Wealth Intelligence', 'Risk Intelligence', 'Business Finance'].map((item) => (
                  <li key={item}>
                    <a 
                      href="#solutions" 
                      onClick={() => sound.playClick(900)}
                      className="hover:text-fintech-blue hover:underline transition-colors block"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Column 2: COMPANY */}
            <div className="space-y-3">
              <div className="font-extrabold text-fintech-black uppercase tracking-wider pb-1 border-b border-fintech-black/20">
                [COMPANY]
              </div>
              <ul className="space-y-2.5 text-fintech-muted">
                {['About', 'Mission', 'Careers', 'Contact'].map((item) => (
                  <li key={item}>
                    <a 
                      href="#mission" 
                      onClick={() => sound.playClick(900)}
                      className="hover:text-fintech-blue hover:underline transition-colors block"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Column 3: RESOURCES */}
            <div className="space-y-3">
              <div className="font-extrabold text-fintech-black uppercase tracking-wider pb-1 border-b border-fintech-black/20">
                [RESOURCES]
              </div>
              <ul className="space-y-2.5 text-fintech-muted">
                {['Insights', 'Blog', 'Research', 'Help Center'].map((item) => (
                  <li key={item}>
                    <a 
                      href="#intelligence" 
                      onClick={() => sound.playClick(900)}
                      className="hover:text-fintech-blue hover:underline transition-colors block"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            {/* Column 4: LEGAL */}
            <div className="space-y-3">
              <div className="font-extrabold text-fintech-black uppercase tracking-wider pb-1 border-b border-fintech-black/20">
                [LEGAL]
              </div>
              <ul className="space-y-2.5 text-fintech-muted">
                {['Privacy', 'Security', 'Terms', 'Compliance'].map((item) => (
                  <li key={item}>
                    <a 
                      href="#" 
                      onClick={(e) => {
                        e.preventDefault();
                        sound.playClick(900);
                      }}
                      className="hover:text-fintech-blue hover:underline transition-colors block"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

          </div>

        </div>

        {/* Bottom Bar: Copyright & Back to Top */}
        <div className="pt-8 flex flex-wrap items-center justify-between gap-4 font-mono text-xs text-fintech-muted">
          <div className="flex items-center space-x-3">
            <span className="font-bold text-fintech-black">© 2026 LEGACYAI. ALL RIGHTS RESERVED.</span>
            <span>•</span>
            <span className="hidden sm:inline">FINANCIAL CLARITY PROTOCOL V2.6</span>
          </div>

          <div className="flex items-center space-x-6">
            <div className="hidden md:flex items-center space-x-2 text-[11px]">
              <ShieldCheck size={14} className="text-emerald-600" />
              <span>SOC-2 CERTIFIED AUDITED INFRASTRUCTURE</span>
            </div>

            <button
              onClick={scrollToTop}
              className="brutal-btn border border-fintech-black bg-white px-3 py-1.5 shadow-brutal-sm flex items-center space-x-1.5 text-fintech-black hover:bg-fintech-paper cursor-pointer font-bold"
            >
              <span>TOP</span>
              <ArrowUp size={13} />
            </button>
          </div>
        </div>

      </div>
    </footer>
  );
};
