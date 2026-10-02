import React from 'react';
import { 
  ShieldCheck, 
  Lock, 
  FileSearch, 
  FileCheck2, 
  CheckCircle,
  KeyRound,
  Fingerprint
} from 'lucide-react';
import { sound } from '../utils/audio';

export const Security: React.FC = () => {
  const securityPillars = [
    {
      title: 'BANK-LEVEL SECURITY',
      subtitle: 'ZERO-TRUST INFRASTRUCTURE',
      description: 'Advanced encryption and secure infrastructure.',
      details: 'All data in transit and at rest is sealed using AES-256-GCM and TLS 1.3 cryptographic protocols with hardware security modules (HSM).',
      icon: ShieldCheck,
      spec: '256-BIT AES GCM // HSM BACKED',
      badge: 'MIL-SPEC'
    },
    {
      title: 'PRIVACY FIRST',
      subtitle: 'SOVEREIGN DATA OWNERSHIP',
      description: 'Your financial information remains under your control.',
      details: 'We never monetize, broker, or sell personal financial records. Your data is never ingested into public AI training corpuses.',
      icon: Lock,
      spec: 'ZERO-KNOWLEDGE // NO THIRD-PARTY SHARING',
      badge: 'STRICT ZERO-LOG'
    },
    {
      title: 'TRANSPARENT AI',
      subtitle: 'EXPLAINABLE REASONING',
      description: 'Understand why LegacyAI recommends an action.',
      details: 'Every algorithmic recommendation is backed by a deterministic math log and plain-English breakdown. Zero black-box mystery.',
      icon: FileSearch,
      spec: 'AUDITABLE MATH LOGS // VERIFIED ALPHA',
      badge: '100% EXPLAINABLE'
    },
    {
      title: 'COMPLIANT BY DESIGN',
      subtitle: 'REGULATORY ALIGNMENT',
      description: 'Built with modern financial security principles.',
      details: 'Designed from day one to exceed SEC, FINRA, SOC 2 Type II, ISO 27001, and GDPR enterprise standards with automated compliance reporting.',
      icon: FileCheck2,
      spec: 'SOC 2 TYPE II // ISO 27001 // SEC READY',
      badge: 'CERTIFIED'
    }
  ];

  return (
    <section className="relative bg-tech-grid py-20 border-b-2 border-fintech-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-16">
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <span className="font-mono text-xs font-bold border border-fintech-black bg-white px-2.5 py-1 shadow-brutal-sm">
                [SECTION // 06]
              </span>
              <span className="font-mono text-xs tracking-widest text-fintech-muted uppercase">
                INSTITUTIONAL TRUST &amp; DEFENSE
              </span>
            </div>

            <h2 className="font-display font-extrabold text-4xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tightest uppercase text-fintech-black">
              YOUR FINANCES.<br />
              <span className="text-fintech-blue">YOUR CONTROL.</span>
            </h2>
          </div>

          <div className="flex items-center space-x-3 border-2 border-fintech-black bg-white p-3 shadow-brutal-sm">
            <Fingerprint size={28} className="text-fintech-blue" />
            <div>
              <div className="font-mono text-xs font-bold text-fintech-black">CRYPTOGRAPHIC ATTESTATION</div>
              <div className="font-mono text-[10px] text-fintech-muted">AUDITED BY INDEPENDENT FIRMS</div>
            </div>
          </div>
        </div>

        {/* 4 Architectural Security Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {securityPillars.map((pillar, idx) => {
            const Icon = pillar.icon;

            return (
              <div
                key={pillar.title}
                onMouseEnter={() => sound.playClick(1000 + idx * 70)}
                className="brutal-card border-2 border-fintech-black bg-white p-7 sm:p-8 shadow-brutal flex flex-col justify-between hover:border-fintech-blue transition-all"
              >
                <div>
                  <div className="flex items-center justify-between pb-4 border-b border-fintech-black/15 mb-6">
                    <div className="flex items-center space-x-3">
                      <div className="w-11 h-11 border border-fintech-black bg-fintech-paper flex items-center justify-center text-fintech-black">
                        <Icon size={22} className="text-fintech-blue" />
                      </div>
                      <div>
                        <span className="font-mono text-[9px] uppercase tracking-widest text-fintech-muted block">
                          {pillar.subtitle}
                        </span>
                        <span className="font-mono text-xs font-bold text-fintech-black">
                          SECURITY_PILLAR_0{idx + 1}
                        </span>
                      </div>
                    </div>

                    <span className="font-mono text-[10px] font-bold border border-fintech-black px-2 py-0.5 bg-fintech-paper">
                      {pillar.badge}
                    </span>
                  </div>

                  <h3 className="font-display font-extrabold text-2xl tracking-tight text-fintech-black mb-2">
                    {pillar.title}
                  </h3>

                  <p className="text-base font-semibold text-fintech-black mb-3">
                    {pillar.description}
                  </p>

                  <p className="text-xs text-fintech-muted leading-relaxed mb-6 font-sans">
                    {pillar.details}
                  </p>
                </div>

                <div className="pt-4 border-t border-fintech-black/20 flex items-center justify-between font-mono text-[10px]">
                  <div className="flex items-center space-x-1.5 text-emerald-800 font-semibold">
                    <CheckCircle size={13} />
                    <span>{pillar.spec}</span>
                  </div>
                  <KeyRound size={13} className="text-fintech-black/40" />
                </div>
              </div>
            );
          })}
        </div>

        {/* Security Seals Strip */}
        <div className="mt-12 border border-fintech-black/30 bg-white p-6 grid grid-cols-2 sm:grid-cols-4 gap-6 text-center font-mono">
          <div className="border-r border-fintech-black/20 last:border-r-0">
            <div className="text-xl font-display font-black text-fintech-black">SOC 2</div>
            <div className="text-[10px] text-fintech-muted uppercase mt-0.5">Type II Certified</div>
          </div>
          <div className="border-r border-fintech-black/20 last:border-r-0">
            <div className="text-xl font-display font-black text-fintech-black">ISO 27001</div>
            <div className="text-[10px] text-fintech-muted uppercase mt-0.5">Information Security</div>
          </div>
          <div className="border-r border-fintech-black/20 last:border-r-0">
            <div className="text-xl font-display font-black text-fintech-black">FINRA</div>
            <div className="text-[10px] text-fintech-muted uppercase mt-0.5">Compliant Architecture</div>
          </div>
          <div>
            <div className="text-xl font-display font-black text-fintech-black">99.99%</div>
            <div className="text-[10px] text-fintech-muted uppercase mt-0.5">SLA Uptime Guarantee</div>
          </div>
        </div>

      </div>
    </section>
  );
};
