import React from 'react';
import { 
  ArrowRight, 
  Volume2, 
  VolumeX, 
  Star, 
  Sparkles, 
  Terminal,
  Layers
} from 'lucide-react';
import { HeroVisual } from './HeroVisual';
import { sound } from '../utils/audio';

interface HeroProps {
  onOpenGetStarted: () => void;
  onExplorePlatform: () => void;
  soundEnabled: boolean;
  onToggleSound: () => boolean;
}

export const Hero: React.FC<HeroProps> = ({
  onOpenGetStarted,
  onExplorePlatform,
  soundEnabled,
  onToggleSound
}) => {
  return (
    <section className="relative bg-tech-grid border-b-2 border-fintech-black pt-8 pb-16 lg:py-20 overflow-hidden">
      {/* Decorative coordinate crosshairs */}
      <div className="hidden lg:block absolute top-6 left-8 font-mono text-[10px] text-fintech-muted uppercase tracking-widest">
        INDEX // 001.00 - HERO_DISPATCH
      </div>
      <div className="hidden lg:block absolute top-6 right-8 font-mono text-[10px] text-fintech-muted uppercase tracking-widest">
        SYSTEM STATUS: ONLINE
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 items-center">
          
          {/* LEFT SIDE: Editorial Typography & Actions */}
          <div className="lg:col-span-6 xl:col-span-7 flex flex-col justify-center space-y-6">
            
            {/* Category / Platform Tag */}
            <div className="inline-flex items-center space-x-2 border border-fintech-black bg-white px-3 py-1 shadow-brutal-sm self-start">
              <Terminal size={13} className="text-fintech-blue" />
              <span className="font-mono text-xs font-bold uppercase tracking-wider text-fintech-black">
                LegacyAI Finance Platform
              </span>
              <span className="w-1.5 h-1.5 bg-fintech-blue rounded-full animate-ping"></span>
            </div>

            {/* Dominant Editorial Headline */}
            <h1 className="font-display font-extrabold text-5xl sm:text-7xl lg:text-8xl xl:text-[88px] leading-[0.92] tracking-tightest text-fintech-black uppercase select-none">
              <span className="block">INTELLIGENT</span>
              <span className="block">FINANCE,</span>
              <span className="block text-fintech-blue">AI-POWERED</span>
              <span className="block">GROWTH.</span>
            </h1>

            {/* Monospace Statement with Thin Vertical Black Rule */}
            <div className="flex items-stretch space-x-4 pt-2">
              <div className="w-0.5 bg-fintech-black shrink-0"></div>
              <p className="font-mono text-xs sm:text-sm font-semibold uppercase tracking-wider text-fintech-black leading-relaxed max-w-lg">
                MAKING EVERY FINANCIAL DECISION SMARTER, CLEARER &amp; MORE STRATEGIC.
              </p>
            </div>

            {/* Hero Description */}
            <p className="text-base sm:text-lg text-fintech-muted font-sans font-normal max-w-xl leading-relaxed">
              LegacyAI combines artificial intelligence, financial intelligence, and real-time insights to help people and businesses make smarter financial decisions.
            </p>

            {/* Hero Buttons: Tactical Brutalist styling */}
            <div className="flex flex-wrap items-center gap-4 pt-4">
              
              {/* PRIMARY BUTTON: EXPLORE PLATFORM */}
              <button
                onClick={() => {
                  sound.playClick(1000);
                  onExplorePlatform();
                }}
                className="group brutal-btn relative border-2 border-fintech-black bg-white p-1 shadow-brutal cursor-pointer"
              >
                <div className="border border-fintech-black px-6 py-3.5 bg-white flex items-center space-x-3 transition-colors group-hover:bg-fintech-paper">
                  <span className="font-mono text-xs sm:text-sm font-bold tracking-wider text-fintech-black uppercase">
                    EXPLORE PLATFORM
                  </span>
                  <ArrowRight size={16} className="text-fintech-black transition-transform group-hover:translate-x-1" />
                </div>
              </button>

              {/* SECONDARY BUTTON: GET STARTED */}
              <button
                onClick={() => {
                  sound.playChime();
                  onOpenGetStarted();
                }}
                className="brutal-btn border-2 border-fintech-black bg-fintech-black text-white px-7 py-4 font-mono text-xs sm:text-sm font-bold tracking-wider uppercase shadow-brutal flex items-center space-x-2.5 cursor-pointer hover:bg-fintech-blue hover:border-fintech-black"
              >
                <span>GET STARTED</span>
                <Sparkles size={15} className="text-amber-400" />
              </button>

            </div>

            {/* Micro-Interaction Element & Social Proof Card at Bottom-Left */}
            <div className="pt-6 flex flex-wrap items-center gap-4">
              
              {/* Floating Circular Audio/Accessibility Button */}
              <button
                onClick={() => {
                  const nowEnabled = onToggleSound();
                  if (nowEnabled) sound.playChime();
                }}
                title={soundEnabled ? 'Disable Tactile Sound Synthesis' : 'Enable Tactile Sound Synthesis'}
                className="group brutal-btn w-12 h-12 rounded-full border-2 border-fintech-black bg-white shadow-brutal flex items-center justify-center cursor-pointer hover:bg-fintech-paper"
              >
                {soundEnabled ? (
                  <Volume2 size={18} className="text-fintech-blue group-hover:scale-110 transition-transform" />
                ) : (
                  <VolumeX size={18} className="text-fintech-muted group-hover:scale-110 transition-transform" />
                )}
              </button>

              {/* Compact Social-Proof Interaction Card */}
              <div 
                onClick={() => {
                  sound.playClick(1200);
                  onExplorePlatform();
                }}
                className="brutal-card border border-fintech-black bg-white px-4 py-2.5 shadow-brutal-sm flex items-center space-x-3 cursor-pointer hover:border-fintech-blue"
              >
                <div className="flex text-amber-500 space-x-0.5">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={13} fill="currentColor" stroke="none" />
                  ))}
                </div>
                <div className="h-4 w-px bg-fintech-black/30"></div>
                <div className="font-mono text-[11px] font-bold tracking-wider text-fintech-black uppercase">
                  TRUSTED BY 12,000+ USERS
                </div>
              </div>

              {/* Extra Brutalist Metric Tag */}
              <div className="hidden sm:flex items-center space-x-1.5 font-mono text-[10px] text-fintech-muted border border-fintech-black/20 px-2.5 py-2 bg-fintech-paper">
                <Layers size={12} className="text-fintech-black" />
                <span>ASSETS MANAGED: $4.2B+</span>
              </div>

            </div>

          </div>

          {/* RIGHT SIDE: Fintech Visual Container */}
          <div className="lg:col-span-6 xl:col-span-5 flex justify-center lg:justify-end">
            <HeroVisual />
          </div>

        </div>
      </div>
    </section>
  );
};
