import React, { useState } from 'react';
import { 
  Link2, 
  BarChart3, 
  Brain, 
  CheckCircle, 
  ChevronRight
} from 'lucide-react';
import { sound } from '../utils/audio';

export const HowItWorks: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(0);

  const steps = [
    {
      number: '01',
      title: 'CONNECT',
      label: 'ZERO-KNOWLEDGE INGESTION',
      description: 'Connect your financial accounts and data.',
      details: 'Instant synchronization across banks, brokerages, crypto custodians, and business ledgers via read-only military-grade cryptographic APIs.',
      icon: Link2,
      output: 'SCHEMA // NORMALIZED LEDGER'
    },
    {
      number: '02',
      title: 'ANALYZE',
      label: 'PATTERN RECOGNITION',
      description: 'LegacyAI analyzes your financial behavior and patterns.',
      details: 'Deep neural networks detect hidden cash drag, recurring micro-leakages, tax inefficiencies, and correlations across asset classes.',
      icon: BarChart3,
      output: 'METRIC // BEHAVIORAL GRAPH'
    },
    {
      number: '03',
      title: 'UNDERSTAND',
      label: 'SYNTHESIS & ABSTRACTION',
      description: 'AI transforms complex information into simple insights.',
      details: 'Raw financial noise is synthesized into plain-English tactical insights, interactive visual projections, and deterministic scenario models.',
      icon: Brain,
      output: 'INSIGHT // EXPLAINABLE AI'
    },
    {
      number: '04',
      title: 'ACT',
      label: 'SOVEREIGN EXECUTION',
      description: 'Receive personalized recommendations and take action.',
      details: 'One-click execution of portfolio rebalancing, high-yield reallocations, and automated risk defenses with full human-in-the-loop control.',
      icon: CheckCircle,
      output: 'ALPHA // VERIFIED EXECUTION'
    }
  ];

  return (
    <section id="how-it-works" className="relative bg-white py-20 border-b-2 border-fintech-black overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-16">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <span className="font-mono text-xs font-bold border border-fintech-black bg-white px-2.5 py-1 shadow-brutal-sm">
                [SECTION // 05]
              </span>
              <span className="font-mono text-xs tracking-widest text-fintech-muted uppercase">
                THE INTELLIGENCE PIPELINE
              </span>
            </div>

            <h2 className="font-display font-extrabold text-4xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tightest uppercase text-fintech-black">
              FROM DATA<br />
              TO <span className="text-fintech-blue">DECISION.</span>
            </h2>
          </div>

          <p className="max-w-md font-sans text-sm sm:text-base text-fintech-muted leading-relaxed">
            A continuous, deterministic 4-stage feedback loop that turns raw transactional signals into strategic wealth expansion.
          </p>
        </div>

        {/* Horizontal Process Container with Connecting Line */}
        <div className="relative">
          
          {/* Architectural Connecting Line (Desktop) */}
          <div className="hidden lg:block absolute top-[62px] left-8 right-8 h-[2px] bg-fintech-black z-0"></div>

          {/* 4 Steps Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
            {steps.map((step, idx) => {
              const Icon = step.icon;
              const isActive = activeStep === idx;

              return (
                <div
                  key={step.number}
                  onMouseEnter={() => {
                    sound.playClick(900 + idx * 90);
                    setActiveStep(idx);
                  }}
                  className={`brutal-card border-2 border-fintech-black bg-white p-6 shadow-brutal flex flex-col justify-between transition-all duration-150 cursor-pointer ${
                    isActive ? 'ring-2 ring-fintech-blue ring-offset-2' : ''
                  }`}
                >
                  <div>
                    {/* Step Header with Node Circle & Number */}
                    <div className="flex items-center justify-between mb-6">
                      <div className="w-12 h-12 border-2 border-fintech-black bg-white flex items-center justify-center font-mono font-black text-base text-fintech-black shadow-brutal-sm">
                        {step.number}
                      </div>

                      <div className="w-9 h-9 border border-fintech-black bg-fintech-paper flex items-center justify-center text-fintech-black">
                        <Icon size={16} className={isActive ? 'text-fintech-blue' : 'text-fintech-black'} />
                      </div>
                    </div>

                    {/* Step Subtitle */}
                    <div className="font-mono text-[9px] uppercase tracking-widest text-fintech-muted mb-1">
                      {step.label}
                    </div>

                    {/* Step Title */}
                    <h3 className="font-display font-black text-2xl tracking-tight text-fintech-black mb-2">
                      {step.title}
                    </h3>

                    {/* Primary Statement */}
                    <p className="text-sm font-semibold text-fintech-black mb-3 leading-snug">
                      &ldquo;{step.description}&rdquo;
                    </p>

                    {/* Deep Detail */}
                    <p className="text-xs text-fintech-muted leading-relaxed mb-4">
                      {step.details}
                    </p>
                  </div>

                  {/* Step Output Tag */}
                  <div className="pt-3 border-t border-fintech-black/15 flex items-center justify-between font-mono text-[10px]">
                    <span className="text-fintech-muted">{step.output}</span>
                    <ChevronRight size={14} className={isActive ? 'text-fintech-blue translate-x-1' : 'text-fintech-black'} />
                  </div>

                </div>
              );
            })}
          </div>

        </div>

        {/* Process Metric Bar */}
        <div className="mt-12 border-2 border-fintech-black bg-fintech-paper p-4 sm:p-6 shadow-brutal flex flex-wrap items-center justify-between gap-4 font-mono text-xs">
          <div className="flex items-center space-x-3">
            <div className="w-2.5 h-2.5 bg-emerald-500 rounded-full animate-pulse"></div>
            <span className="font-bold text-fintech-black">CONTINUOUS EXECUTION LATENCY:</span>
            <span className="text-fintech-blue font-bold">&lt; 150 MILLISECONDS</span>
          </div>
          <div className="flex items-center space-x-4 text-fintech-muted text-[11px]">
            <span>SOC-2 TYPE II</span>
            <span>•</span>
            <span>256-BIT AES GCM</span>
            <span>•</span>
            <span>REST &amp; FIX PROTOCOL COMPATIBLE</span>
          </div>
        </div>

      </div>
    </section>
  );
};
