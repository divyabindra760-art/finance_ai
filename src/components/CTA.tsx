import React from 'react';
import { ArrowRight, Sparkles, Terminal } from 'lucide-react';
import { sound } from '../utils/audio';

interface CTAProps {
  onOpenGetStarted: () => void;
}

export const CTA: React.FC<CTAProps> = ({ onOpenGetStarted }) => {
  return (
    <section className="relative bg-fintech-black text-white py-24 sm:py-32 border-b-2 border-fintech-black overflow-hidden">
      {/* Subtle dark technical grid */}
      <div className="absolute inset-0 bg-tech-grid-dark opacity-70 pointer-events-none"></div>

      {/* Decorative architectural markers */}
      <div className="absolute top-6 left-8 font-mono text-[10px] text-white/40 uppercase tracking-widest hidden md:block">
        [CALL_TO_ACTION // GATEWAY_07]
      </div>
      <div className="absolute top-6 right-8 font-mono text-[10px] text-white/40 uppercase tracking-widest hidden md:block">
        DEPLOYMENT: INSTANT // 2-MIN SETUP
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-4xl mx-auto text-center flex flex-col items-center">
          
          {/* Subtle tag */}
          <div className="inline-flex items-center space-x-2 border border-white/30 bg-white/5 px-3 py-1 mb-8 shadow-brutal-white">
            <Terminal size={12} className="text-fintech-blue" />
            <span className="font-mono text-xs font-bold uppercase tracking-widest text-white">
              LEGACYAI ALPHA REVOLUTION
            </span>
          </div>

          {/* White Dominant Headline */}
          <h2 className="font-display font-black text-5xl sm:text-7xl lg:text-8xl leading-[0.9] tracking-tightest uppercase text-white mb-6 select-none">
            BUILD A<br />
            SMARTER<br />
            <span className="text-fintech-blue">FINANCIAL</span><br />
            FUTURE.
          </h2>

          {/* Small Text */}
          <p className="font-sans text-base sm:text-xl text-white/80 max-w-xl mb-10 leading-relaxed">
            Start turning financial complexity into intelligent opportunity.
          </p>

          {/* Large White Bordered Tactile Button */}
          <div className="flex flex-wrap items-center justify-center gap-4">
            <button
              onClick={() => {
                sound.playChime();
                onOpenGetStarted();
              }}
              className="group brutal-btn relative border-2 border-white bg-transparent p-1 shadow-brutal-white cursor-pointer transition-transform hover:-translate-x-1 hover:-translate-y-1"
            >
              <div className="border border-white bg-white text-fintech-black px-8 sm:px-10 py-4 sm:py-5 flex items-center space-x-4 transition-colors group-hover:bg-fintech-paper">
                <span className="font-mono text-sm sm:text-base font-extrabold tracking-wider uppercase">
                  START WITH LEGACYAI
                </span>
                <ArrowRight size={20} className="text-fintech-black transition-transform group-hover:translate-x-1.5" />
              </div>
            </button>
          </div>

          {/* Micro Security Guarantee */}
          <div className="mt-10 flex flex-wrap items-center justify-center gap-6 font-mono text-xs text-white/60">
            <div className="flex items-center space-x-2">
              <Sparkles size={13} className="text-amber-400" />
              <span>NO CREDIT CARD REQUIRED TO START</span>
            </div>
            <span>•</span>
            <span>2-MINUTE ONBOARDING</span>
            <span>•</span>
            <span>CANCEL ANYTIME</span>
          </div>

        </div>
      </div>
    </section>
  );
};
