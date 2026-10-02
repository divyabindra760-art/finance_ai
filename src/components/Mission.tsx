import React from 'react';
import { Eye, Brain, Shield, ArrowUpRight } from 'lucide-react';
import { sound } from '../utils/audio';

export const Mission: React.FC = () => {
  const cards = [
    {
      number: '01',
      title: 'CLARITY',
      subtitle: 'DATA SIMPLIFICATION ENGINE',
      description: 'Turn complex financial information into understandable insights.',
      detail: 'Reconciles fragmented accounts, tax liabilities, and hidden broker fees into a unified, high-definition financial model.',
      icon: Eye,
      tag: 'VISIBILITY // 100%'
    },
    {
      number: '02',
      title: 'INTELLIGENCE',
      subtitle: 'PROACTIVE NEURAL REASONING',
      description: 'Use AI to identify opportunities, risks and patterns.',
      detail: 'Continuous algorithmic modeling surfaces alpha generation triggers, rebalancing anomalies, and market regime changes in real time.',
      icon: Brain,
      tag: 'PREDICTIVE // 99.4%'
    },
    {
      number: '03',
      title: 'CONTROL',
      subtitle: 'SOVEREIGN DECISION ARCHITECTURE',
      description: 'Make confident decisions with real-time financial intelligence.',
      detail: 'Simulate high-impact capital allocation scenarios before execution with verifiable mathematical certainty and downside limits.',
      icon: Shield,
      tag: 'EXECUTION // INSTANT'
    }
  ];

  return (
    <section id="mission" className="relative bg-tech-grid py-20 border-b-2 border-fintech-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Index Header */}
        <div className="flex items-center space-x-3 mb-6">
          <span className="font-mono text-xs font-bold border border-fintech-black bg-white px-2.5 py-1 shadow-brutal-sm">
            [SECTION // 02]
          </span>
          <span className="font-mono text-xs tracking-widest text-fintech-muted uppercase">
            CORE PHILOSOPHY &amp; MISSION
          </span>
        </div>

        {/* Heading & Supporting Text Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start mb-16">
          <div className="lg:col-span-8">
            <h2 className="font-display font-extrabold text-4xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tightest uppercase text-fintech-black">
              FINANCE SHOULD<br />
              WORK FOR <span className="text-fintech-blue">YOU.</span>
            </h2>
          </div>

          <div className="lg:col-span-4 lg:pt-2 border-l-2 border-fintech-black/20 pl-6">
            <p className="text-base sm:text-lg text-fintech-black font-sans leading-relaxed">
              Traditional financial systems overwhelm people with complexity. LegacyAI turns financial data into clear, intelligent and actionable decisions.
            </p>
            <div className="mt-4 font-mono text-xs text-fintech-muted">
              REF: ARCHITECTURE SPEC v2.6 // ZERO COMPROMISE
            </div>
          </div>
        </div>

        {/* Three Architectural Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {cards.map((card) => {
            const Icon = card.icon;
            return (
              <div
                key={card.number}
                onMouseEnter={() => sound.playClick(900 + parseInt(card.number) * 100)}
                className="group brutal-card relative border-2 border-fintech-black bg-white p-6 sm:p-8 shadow-brutal flex flex-col justify-between hover:border-fintech-blue transition-all"
              >
                {/* Corner bracket detail */}
                <span className="absolute top-2 right-2 font-mono text-xs text-fintech-black/40 group-hover:text-fintech-blue">
                  +
                </span>

                <div>
                  {/* Top Bar with Number and Minimal Icon */}
                  <div className="flex items-center justify-between pb-4 border-b border-fintech-black/20 mb-6">
                    <span className="font-mono text-3xl font-extrabold text-fintech-black group-hover:text-fintech-blue transition-colors">
                      {card.number}
                    </span>
                    <div className="w-10 h-10 border border-fintech-black bg-fintech-paper flex items-center justify-center group-hover:bg-fintech-black group-hover:text-white transition-colors">
                      <Icon size={20} />
                    </div>
                  </div>

                  {/* Subtitle / Spec */}
                  <div className="font-mono text-[10px] uppercase tracking-widest text-fintech-muted mb-1">
                    {card.subtitle}
                  </div>

                  {/* Card Title */}
                  <h3 className="font-display font-extrabold text-2xl tracking-tight text-fintech-black mb-3">
                    {card.title}
                  </h3>

                  {/* Primary Description */}
                  <p className="text-sm sm:text-base font-medium text-fintech-black mb-4 leading-relaxed">
                    &ldquo;{card.description}&rdquo;
                  </p>

                  {/* Detailed Context */}
                  <p className="text-xs text-fintech-muted leading-relaxed">
                    {card.detail}
                  </p>
                </div>

                {/* Bottom Architectural Tag */}
                <div className="mt-8 pt-4 border-t border-fintech-black/10 flex items-center justify-between font-mono text-[10px]">
                  <span className="text-fintech-muted">{card.tag}</span>
                  <div className="flex items-center space-x-1 text-fintech-black group-hover:text-fintech-blue font-bold">
                    <span>EXPLORE</span>
                    <ArrowUpRight size={12} className="group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
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
