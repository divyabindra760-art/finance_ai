import React, { useState } from 'react';
import { 
  Bot, 
  LineChart, 
  ShieldAlert, 
  Briefcase, 
  ArrowUpRight, 
  CheckCircle2,
  Layers
} from 'lucide-react';
import { sound } from '../utils/audio';

export const Solutions: React.FC = () => {
  const [activeCard, setActiveCard] = useState<number | null>(null);

  const solutions = [
    {
      number: '01',
      title: 'AI FINANCIAL ADVISOR',
      tag: 'PERSONALIZED INTEL',
      description: 'Personalized financial intelligence powered by AI.',
      extended: 'Real-time conversational wealth guidance tailored to your specific liquidity requirements, horizon, and tax status.',
      icon: Bot,
      features: [
        'Context-aware portfolio rebalancing',
        'Tax-loss harvesting triggers',
        '24/7 autonomous financial monitoring'
      ]
    },
    {
      number: '02',
      title: 'WEALTH OPTIMIZATION',
      tag: 'ALPHA HARVESTING',
      description: 'Identify opportunities to improve financial outcomes.',
      extended: 'Algorithmic yield discovery across global sovereign debt, automated index replication, and institutional fee compression.',
      icon: LineChart,
      features: [
        'Dynamic cash drag elimination',
        'Private equity / real asset tracking',
        'Automated dividend compounding'
      ]
    },
    {
      number: '03',
      title: 'RISK INTELLIGENCE',
      tag: 'PREDICTIVE DEFENSE',
      description: 'Understand financial risks before they become problems.',
      extended: 'Stress-test portfolios against sudden inflation spikes, liquidity crunches, and geopolitical regime shocks with deep predictive modeling.',
      icon: ShieldAlert,
      features: [
        'Monte Carlo volatility stress testing',
        'Concentration risk alerts',
        'Tail-risk algorithmic hedging'
      ]
    },
    {
      number: '04',
      title: 'BUSINESS FINANCE',
      tag: 'INSTITUTIONAL SUITE',
      description: 'Intelligent financial insights for modern businesses.',
      extended: 'Cash-flow forecasting, automated treasury management, and intelligent working capital optimization for forward-thinking enterprises.',
      icon: Briefcase,
      features: [
        'Automated runway projection',
        'Multi-entity cross-border treasury',
        'Real-time vendor cost intelligence'
      ]
    }
  ];

  return (
    <section id="solutions" className="relative bg-white py-20 border-b-2 border-fintech-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-12">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <span className="font-mono text-xs font-bold border border-fintech-black bg-white px-2.5 py-1 shadow-brutal-sm">
                [SECTION // 03]
              </span>
              <span className="font-mono text-xs tracking-widest text-fintech-muted uppercase">
                COMPREHENSIVE CAPABILITIES
              </span>
            </div>

            <h2 className="font-display font-extrabold text-4xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tightest uppercase text-fintech-black">
              ONE INTELLIGENT<br />
              FINANCIAL ECOSYSTEM.
            </h2>
          </div>

          <div className="border border-fintech-black p-4 bg-fintech-paper max-w-sm font-mono text-xs shadow-brutal-sm">
            <div className="flex items-center space-x-2 text-fintech-black font-bold mb-1">
              <Layers size={14} className="text-fintech-blue" />
              <span>UNIFIED ARCHITECTURE</span>
            </div>
            <p className="text-fintech-muted text-[11px] leading-relaxed">
              Modular components running concurrently on a high-throughput deterministic neural ledger.
            </p>
          </div>
        </div>

        {/* 4 Premium Solution Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {solutions.map((item, idx) => {
            const Icon = item.icon;
            const isHovered = activeCard === idx;

            return (
              <div
                key={item.number}
                onMouseEnter={() => {
                  sound.playClick(950 + idx * 80);
                  setActiveCard(idx);
                }}
                onMouseLeave={() => setActiveCard(null)}
                className={`group brutal-card relative border-2 border-fintech-black bg-white p-7 sm:p-9 shadow-brutal flex flex-col justify-between transition-all duration-200 ${
                  isHovered ? 'border-fintech-blue' : ''
                }`}
              >
                {/* Corner Decoration */}
                <div className="absolute top-3 right-3 font-mono text-xs text-fintech-black/30 group-hover:text-fintech-blue">
                  [{item.number}]
                </div>

                <div>
                  {/* Top line with Icon and Tag */}
                  <div className="flex items-center space-x-3 mb-6">
                    <div className="w-12 h-12 border-2 border-fintech-black bg-fintech-paper flex items-center justify-center group-hover:bg-fintech-black group-hover:text-white transition-colors">
                      <Icon size={22} className="transition-transform group-hover:scale-110" />
                    </div>
                    <div>
                      <span className="font-mono text-[10px] tracking-widest text-fintech-muted uppercase block">
                        {item.tag}
                      </span>
                      <span className="font-mono text-xs font-bold text-fintech-black">
                        MODULE_0{idx + 1}
                      </span>
                    </div>
                  </div>

                  {/* Heading */}
                  <h3 className="font-display font-extrabold text-2xl sm:text-3xl tracking-tight text-fintech-black mb-3 group-hover:text-fintech-blue transition-colors">
                    {item.title}
                  </h3>

                  {/* Highlighted Lead */}
                  <p className="text-base font-semibold text-fintech-black mb-2">
                    {item.description}
                  </p>

                  {/* Extended Context */}
                  <p className="text-sm text-fintech-muted leading-relaxed mb-6">
                    {item.extended}
                  </p>

                  {/* Feature Checklist */}
                  <div className="space-y-2 border-t border-fintech-black/15 pt-4 mb-6 font-mono text-xs">
                    {item.features.map((feat, fIdx) => (
                      <div key={fIdx} className="flex items-center space-x-2 text-fintech-black">
                        <CheckCircle2 size={13} className="text-fintech-blue shrink-0" />
                        <span>{feat}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Card Action Link */}
                <div className="pt-4 border-t border-fintech-black/20 flex items-center justify-between font-mono text-xs">
                  <span className="text-fintech-muted">INTEGRATION: INSTANT API</span>
                  <div className="flex items-center space-x-1.5 font-bold text-fintech-black group-hover:text-fintech-blue">
                    <span>LEARN SPECIFICATION</span>
                    <ArrowUpRight size={14} className="transition-transform group-hover:translate-x-1 group-hover:-translate-y-1" />
                  </div>
                </div>

              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
