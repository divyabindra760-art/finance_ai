import React, { useState } from 'react';
import { 
  User, 
  Target, 
  Cpu, 
  Box, 
  Workflow, 
  FileText, 
  ArrowUpRight, 
  Menu, 
  X,
  Volume2,
  VolumeX
} from 'lucide-react';
import { sound } from '../utils/audio';

interface NavbarProps {
  onOpenGetStarted: () => void;
  soundEnabled: boolean;
  onToggleSound: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ 
  onOpenGetStarted, 
  soundEnabled, 
  onToggleSound 
}) => {
  const [activeItem, setActiveItem] = useState('SOLUTIONS');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navItems = [
    { label: 'ABOUT', href: '#mission', icon: User },
    { label: 'MISSION', href: '#mission', icon: Target },
    { label: 'SOLUTIONS', href: '#solutions', icon: Cpu },
    { label: 'PRODUCTS', href: '#intelligence', icon: Box },
    { label: 'HOW IT WORKS', href: '#how-it-works', icon: Workflow },
    { label: 'INSIGHTS', href: '#intelligence', icon: FileText },
  ];

  const handleNavClick = (label: string, href: string) => {
    sound.playClick(850);
    setActiveItem(label);
    setMobileMenuOpen(false);
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b-2 border-fintech-black transition-all">
      {/* Top technical coordinate micro-bar */}
      <div className="hidden md:flex justify-between items-center px-6 py-1 border-b border-fintech-black/10 bg-fintech-paper text-[10px] font-mono tracking-widest text-fintech-muted uppercase">
        <div className="flex items-center space-x-4">
          <span>SEC PROTOCOL: ACTIVE // TLS 1.3</span>
          <span className="inline-block w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
          <span>SYSTEM TIME: REALTIME FEED</span>
        </div>
        <div className="flex items-center space-x-6">
          <span>AI ACCELERATOR: ONLINE</span>
          <span>SYS_LATENCY: 14MS</span>
          <button 
            onClick={onToggleSound}
            aria-label="Toggle sound feedback"
            className="flex items-center space-x-1 hover:text-fintech-black transition-colors font-mono cursor-pointer"
          >
            {soundEnabled ? <Volume2 size={12} className="text-fintech-blue" /> : <VolumeX size={12} />}
            <span>{soundEnabled ? 'AUDIO: ON' : 'AUDIO: OFF'}</span>
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* LEFT: Boxed LEGACYAI Wordmark */}
        <a 
          href="#" 
          onClick={() => sound.playClick(1000)}
          className="group relative inline-block"
        >
          {/* Double-border frame box with offset shadow */}
          <div className="p-1 border-2 border-fintech-black bg-white shadow-brutal transition-transform group-hover:-translate-x-0.5 group-hover:-translate-y-0.5">
            <div className="border border-fintech-black px-4 py-2 flex items-center space-x-2 bg-white">
              <div className="w-2.5 h-2.5 bg-fintech-blue border border-fintech-black"></div>
              <span className="font-display font-extrabold text-xl sm:text-2xl tracking-tight text-fintech-black">
                LEGACY<span className="text-fintech-blue">AI</span>
              </span>
              <span className="hidden sm:inline-block text-[9px] font-mono border border-fintech-black/40 px-1 py-0.5 bg-fintech-paper text-fintech-muted">
                v2.6
              </span>
            </div>
          </div>
        </a>

        {/* CENTER / RIGHT: Navigation Items */}
        <nav className="hidden xl:flex items-center space-x-1 font-mono text-xs font-semibold tracking-wider">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeItem === item.label;

            return (
              <a
                key={item.label}
                href={item.href}
                onClick={(e) => {
                  e.preventDefault();
                  handleNavClick(item.label, item.href);
                }}
                className={`flex items-center space-x-1.5 px-3 py-2 transition-all duration-150 ${
                  isActive
                    ? 'bg-fintech-black text-white shadow-brutal-sm'
                    : 'text-fintech-black hover:bg-fintech-paper hover:text-fintech-blue'
                }`}
              >
                <Icon size={14} className={isActive ? 'text-white' : 'text-fintech-muted'} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>

        {/* RIGHTMOST CTA BUTTON */}
        <div className="hidden md:flex items-center space-x-3">
          <button
            onClick={() => {
              sound.playChime();
              onOpenGetStarted();
            }}
            className="brutal-btn border-2 border-fintech-black bg-fintech-black text-white px-5 py-2.5 text-xs font-mono font-bold tracking-wider shadow-brutal flex items-center space-x-2 cursor-pointer hover:bg-fintech-blue hover:border-fintech-black"
          >
            <span>GET STARTED</span>
            <ArrowUpRight size={15} />
          </button>
        </div>

        {/* Mobile menu trigger */}
        <div className="flex items-center space-x-2 xl:hidden">
          <button
            onClick={onToggleSound}
            aria-label="Toggle sound"
            className="p-2 border border-fintech-black text-xs font-mono flex items-center"
          >
            {soundEnabled ? <Volume2 size={16} /> : <VolumeX size={16} />}
          </button>
          
          <button
            onClick={() => {
              sound.playClick();
              setMobileMenuOpen(!mobileMenuOpen);
            }}
            aria-label="Toggle mobile menu"
            className="p-2 border-2 border-fintech-black shadow-brutal-sm bg-white hover:bg-fintech-paper"
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* MOBILE DRAWER */}
      {mobileMenuOpen && (
        <div className="xl:hidden border-t-2 border-fintech-black bg-white px-4 pt-3 pb-6 shadow-brutal-lg animate-in slide-in-from-top-2">
          <div className="grid grid-cols-1 gap-2 font-mono text-xs mb-4">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeItem === item.label;
              return (
                <a
                  key={item.label}
                  href={item.href}
                  onClick={(e) => {
                    e.preventDefault();
                    handleNavClick(item.label, item.href);
                  }}
                  className={`flex items-center justify-between p-3 border border-fintech-black ${
                    isActive ? 'bg-fintech-black text-white' : 'bg-fintech-paper hover:bg-white'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    <Icon size={16} />
                    <span className="font-bold">{item.label}</span>
                  </div>
                  <span className="text-[10px] opacity-70">[REF // {item.label.slice(0, 3)}]</span>
                </a>
              );
            })}
          </div>

          <button
            onClick={() => {
              sound.playChime();
              setMobileMenuOpen(false);
              onOpenGetStarted();
            }}
            className="w-full brutal-btn border-2 border-fintech-black bg-fintech-black text-white py-3 text-xs font-mono font-bold tracking-wider shadow-brutal flex items-center justify-center space-x-2"
          >
            <span>GET STARTED NOW</span>
            <ArrowUpRight size={16} />
          </button>
        </div>
      )}
    </header>
  );
};
