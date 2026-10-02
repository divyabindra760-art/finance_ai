import React, { useState, useEffect } from 'react';
import { X, Sparkles, ArrowRight, CheckCircle2, Sliders, Shield } from 'lucide-react';
import { sound } from '../utils/audio';

interface GetStartedModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialMode?: 'onboard' | 'simulate';
}

export const GetStartedModal: React.FC<GetStartedModalProps> = ({
  isOpen,
  onClose,
  initialMode = 'onboard'
}) => {
  const [mode, setMode] = useState<'onboard' | 'simulate'>(initialMode);
  const [step, setStep] = useState<number>(1);
  const [capital, setCapital] = useState<string>('$100K - $500K');
  const [goal, setGoal] = useState<string>('Yield Optimization');
  const [email, setEmail] = useState<string>('');
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [isCompleted, setIsCompleted] = useState<boolean>(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        sound.playClick(700);
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleSimulate = () => {
    sound.playClick(900);
    setIsAnalyzing(true);
    setTimeout(() => {
      sound.playChime();
      setIsAnalyzing(false);
      setStep(2);
    }, 1200);
  };

  const handleComplete = (e: React.FormEvent) => {
    e.preventDefault();
    sound.playChime();
    setIsCompleted(true);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-fintech-black/70 backdrop-blur-sm animate-in fade-in duration-150">
      
      {/* Brutalist Modal Container */}
      <div className="relative w-full max-w-2xl border-[3px] border-fintech-black bg-white shadow-brutal-xl p-2">
        
        {/* Corner Brackets */}
        <span className="absolute -top-3 -left-3 font-mono text-sm font-black text-fintech-black bg-white px-1 border border-fintech-black select-none z-20">
          +
        </span>
        <span className="absolute -top-3 -right-3 font-mono text-sm font-black text-fintech-black bg-white px-1 border border-fintech-black select-none z-20">
          +
        </span>
        <span className="absolute -bottom-3 -left-3 font-mono text-sm font-black text-fintech-black bg-white px-1 border border-fintech-black select-none z-20">
          +
        </span>
        <span className="absolute -bottom-3 -right-3 font-mono text-sm font-black text-fintech-black bg-white px-1 border border-fintech-black select-none z-20">
          +
        </span>

        {/* Inner Frame */}
        <div className="border border-fintech-black/30 p-6 sm:p-8 bg-white relative max-h-[85vh] overflow-y-auto">
          
          {/* Header Bar */}
          <div className="flex items-center justify-between pb-4 border-b-2 border-fintech-black mb-6">
            <div className="flex items-center space-x-2.5">
              <div className="w-3 h-3 bg-fintech-blue"></div>
              <span className="font-mono text-xs font-bold uppercase tracking-wider text-fintech-black">
                ONBOARDING DISPATCH // ACCESS GATE
              </span>
            </div>

            <button
              onClick={() => {
                sound.playClick(800);
                onClose();
              }}
              className="p-1.5 border border-fintech-black hover:bg-fintech-black hover:text-white transition-colors cursor-pointer"
            >
              <X size={18} />
            </button>
          </div>

          {!isCompleted ? (
            <div>
              {/* Mode Toggle */}
              <div className="flex border border-fintech-black bg-fintech-paper mb-6 p-0.5 font-mono text-xs shadow-brutal-sm">
                <button
                  type="button"
                  onClick={() => {
                    sound.playClick(900);
                    setMode('onboard');
                  }}
                  className={`flex-1 py-2 font-bold transition-colors ${
                    mode === 'onboard' 
                      ? 'bg-fintech-black text-white' 
                      : 'text-fintech-muted hover:text-fintech-black'
                  }`}
                >
                  01 INSTITUTIONAL ONBOARDING
                </button>
                <button
                  type="button"
                  onClick={() => {
                    sound.playClick(900);
                    setMode('simulate');
                  }}
                  className={`flex-1 py-2 font-bold transition-colors ${
                    mode === 'simulate' 
                      ? 'bg-fintech-black text-white' 
                      : 'text-fintech-muted hover:text-fintech-black'
                  }`}
                >
                  02 INTERACTIVE AI SIMULATOR
                </button>
              </div>

              {mode === 'onboard' ? (
                /* Mode 1: Onboarding Form */
                <form onSubmit={handleComplete} className="space-y-4">
                  <div>
                    <h3 className="font-display font-extrabold text-2xl uppercase tracking-tight text-fintech-black mb-1">
                      INITIATE YOUR FINANCIAL ENGINE
                    </h3>
                    <p className="font-sans text-xs text-fintech-muted leading-relaxed">
                      Direct connectivity to private banking APIs, zero-knowledge data pipelines, and personalized AI advisors.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 font-mono text-xs">
                    <div>
                      <label className="block uppercase font-bold text-fintech-black mb-1">
                        PORTFOLIO / LIQUID ASSETS
                      </label>
                      <select 
                        value={capital}
                        onChange={(e) => setCapital(e.target.value)}
                        className="w-full border-2 border-fintech-black p-2.5 bg-white text-fintech-black font-mono text-xs focus:outline-none focus:ring-2 focus:ring-fintech-blue"
                      >
                        <option>$50K - $250K</option>
                        <option>$250K - $1M</option>
                        <option>$1M - $5M</option>
                        <option>$5M - $25M+</option>
                        <option>Enterprise / Treasury</option>
                      </select>
                    </div>

                    <div>
                      <label className="block uppercase font-bold text-fintech-black mb-1">
                        PRIMARY OBJECTIVE
                      </label>
                      <select 
                        value={goal}
                        onChange={(e) => setGoal(e.target.value)}
                        className="w-full border-2 border-fintech-black p-2.5 bg-white text-fintech-black font-mono text-xs focus:outline-none focus:ring-2 focus:ring-fintech-blue"
                      >
                        <option>Yield Optimization &amp; Alpha</option>
                        <option>Tax Drag Elimination</option>
                        <option>Predictive Risk Hedging</option>
                        <option>Business Treasury Management</option>
                        <option>Multi-Generational Wealth Preservation</option>
                      </select>
                    </div>
                  </div>

                  <div className="pt-2 font-mono text-xs">
                    <label className="block uppercase font-bold text-fintech-black mb-1">
                      OFFICIAL EMAIL ADDRESS
                    </label>
                    <input
                      type="email"
                      required
                      placeholder="name@institution.com or personal@domain.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      className="w-full border-2 border-fintech-black p-3 bg-white text-fintech-black font-sans text-sm focus:outline-none focus:ring-2 focus:ring-fintech-blue"
                    />
                  </div>

                  <div className="pt-4">
                    <button
                      type="submit"
                      className="w-full brutal-btn border-2 border-fintech-black bg-fintech-black text-white py-3.5 font-mono text-xs font-bold uppercase tracking-wider shadow-brutal flex items-center justify-center space-x-2 cursor-pointer hover:bg-fintech-blue hover:border-fintech-black"
                    >
                      <span>GENERATE CREDENTIALS &amp; ENTER</span>
                      <ArrowRight size={16} />
                    </button>
                  </div>
                </form>
              ) : (
                /* Mode 2: Interactive AI Simulator */
                <div className="space-y-4">
                  {step === 1 ? (
                    <div className="space-y-4">
                      <div>
                        <h3 className="font-display font-extrabold text-2xl uppercase tracking-tight text-fintech-black mb-1">
                          REAL-TIME ALPHA SIMULATOR
                        </h3>
                        <p className="font-sans text-xs text-fintech-muted leading-relaxed">
                          Run our deterministic neural model on simulated capital allocations to project 5-year alpha expansion.
                        </p>
                      </div>

                      <div className="p-4 border border-fintech-black bg-fintech-paper font-mono text-xs space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-fintech-muted">SIMULATED ASSETS:</span>
                          <span className="font-bold text-fintech-black">$750,000</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-fintech-muted">PORTFOLIO BETA:</span>
                          <span className="font-bold text-fintech-black">0.68 (LOW SENSITIVITY)</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-fintech-muted">INFLATION HEDGE RATIO:</span>
                          <span className="font-bold text-emerald-700">88.4%</span>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={handleSimulate}
                        disabled={isAnalyzing}
                        className="w-full brutal-btn border-2 border-fintech-black bg-fintech-blue text-white py-3.5 font-mono text-xs font-bold uppercase tracking-wider shadow-brutal flex items-center justify-center space-x-2 cursor-pointer"
                      >
                        {isAnalyzing ? (
                          <>
                            <Sparkles size={16} className="animate-spin" />
                            <span>PROCESSING SYNTHETIC VECTORS...</span>
                          </>
                        ) : (
                          <>
                            <Sliders size={16} />
                            <span>EXECUTE STRESS-TEST &amp; ALPHA RUN</span>
                          </>
                        )}
                      </button>
                    </div>
                  ) : (
                    <div className="space-y-4 animate-in fade-in">
                      <div className="p-4 border-2 border-fintech-black bg-white shadow-brutal-sm font-mono text-xs space-y-2">
                        <div className="flex justify-between items-center border-b border-fintech-black/20 pb-2">
                          <span className="font-bold text-fintech-blue">SIMULATION OUTCOME</span>
                          <span className="text-emerald-700 font-bold">ALPHA GENERATED</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-fintech-muted">PROJECTED 5-YR NET GAIN:</span>
                          <span className="font-bold text-fintech-black text-sm">+$241,850</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-fintech-muted">MAX DRAWDOWN REDUCTION:</span>
                          <span className="font-bold text-emerald-700">-42.6%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-fintech-muted">AI HEALTH SCORE:</span>
                          <span className="font-bold text-fintech-blue">96.4 / 100</span>
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() => setMode('onboard')}
                        className="w-full brutal-btn border-2 border-fintech-black bg-fintech-black text-white py-3.5 font-mono text-xs font-bold uppercase tracking-wider shadow-brutal flex items-center justify-center space-x-2"
                      >
                        <span>SAVE SIMULATION &amp; CREATE ACCOUNT</span>
                        <ArrowRight size={16} />
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Bottom Security Note */}
              <div className="pt-6 border-t border-fintech-black/10 flex items-center justify-between font-mono text-[10px] text-fintech-muted">
                <div className="flex items-center space-x-1.5">
                  <Shield size={12} className="text-fintech-blue" />
                  <span>AES-256 ENCRYPTED SESSION</span>
                </div>
                <span>STATUS: ACTIVE // VERIFIED</span>
              </div>
            </div>
          ) : (
            /* Completed State */
            <div className="text-center py-8 space-y-4 animate-in zoom-in-95">
              <div className="w-14 h-14 border-2 border-fintech-black bg-emerald-50 text-emerald-700 mx-auto flex items-center justify-center shadow-brutal-sm">
                <CheckCircle2 size={32} />
              </div>

              <h3 className="font-display font-extrabold text-3xl uppercase tracking-tight text-fintech-black">
                ACCESS GRANTED
              </h3>

              <p className="font-sans text-sm text-fintech-muted max-w-md mx-auto leading-relaxed">
                Your sandbox environment has been provisioned. A private cryptographic onboarding packet has been dispatched to <strong>{email || 'your registered address'}</strong>.
              </p>

              <div className="pt-4">
                <button
                  type="button"
                  onClick={() => {
                    sound.playClick(900);
                    onClose();
                    setIsCompleted(false);
                  }}
                  className="brutal-btn border-2 border-fintech-black bg-fintech-black text-white px-8 py-3 font-mono text-xs font-bold uppercase tracking-wider shadow-brutal"
                >
                  RETURN TO DASHBOARD
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};
