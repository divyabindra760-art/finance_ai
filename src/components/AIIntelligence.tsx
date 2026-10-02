import React, { useState } from 'react';
import { 
  Check, 
  Sparkles, 
  Sliders, 
  Terminal, 
  Cpu, 
  Maximize2,
  Lock,
  ChevronRight
} from 'lucide-react';
import { sound } from '../utils/audio';

type Timeframe = '1D' | '1W' | '1M' | '1Y' | 'ALL';
type Tab = 'overview' | 'stress' | 'decisions';

export const AIIntelligence: React.FC = () => {
  const [timeframe, setTimeframe] = useState<Timeframe>('1M');
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const [actionApplied, setActionApplied] = useState(false);

  // Timeframe-specific data
  const dataByTf: Record<Timeframe, { total: string; change: string; chartPath: string }> = {
    '1D': { total: '$284,620', change: '+0.38%', chartPath: 'M 0 120 Q 80 110, 160 115 T 320 100 T 480 80' },
    '1W': { total: '$284,620', change: '+2.14%', chartPath: 'M 0 140 Q 100 130, 200 110 T 350 95 T 480 70' },
    '1M': { total: '$284,620', change: '+8.42%', chartPath: 'M 0 150 Q 90 140, 180 120 T 320 85 T 480 40' },
    '1Y': { total: '$284,620', change: '+24.18%', chartPath: 'M 0 170 Q 120 150, 240 100 T 380 60 T 480 25' },
    'ALL': { total: '$284,620', change: '+89.65%', chartPath: 'M 0 180 Q 110 160, 220 90 T 360 45 T 480 15' },
  };

  const handleApplyAction = () => {
    sound.playChime();
    setActionApplied(!actionApplied);
  };

  return (
    <section id="intelligence" className="relative bg-tech-grid py-20 border-b-2 border-fintech-black">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Section Header */}
        <div className="mb-12">
          <div className="flex items-center space-x-3 mb-4">
            <span className="font-mono text-xs font-bold border border-fintech-black bg-white px-2.5 py-1 shadow-brutal-sm">
              [SECTION // 04]
            </span>
            <span className="font-mono text-xs tracking-widest text-fintech-muted uppercase">
              SYNTHETIC REASONING CORE
            </span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-end">
            <div className="lg:col-span-8">
              <h2 className="font-display font-extrabold text-4xl sm:text-6xl lg:text-7xl leading-[0.95] tracking-tightest uppercase text-fintech-black">
                YOUR MONEY.<br />
                <span className="text-fintech-blue">UNDERSTOOD</span> BY AI.
              </h2>
            </div>
            <div className="lg:col-span-4">
              <p className="font-sans text-sm sm:text-base text-fintech-muted leading-relaxed">
                A unified algorithmic cockpit aggregating global macro indicators, personalized cash flow velocity, and deterministic optimization models.
              </p>
            </div>
          </div>
        </div>

        {/* MOCK FINANCIAL INTELLIGENCE INTERFACE */}
        <div className="border-[3px] border-fintech-black bg-white shadow-brutal-xl">
          
          {/* Top Terminal Bar */}
          <div className="border-b-2 border-fintech-black bg-fintech-black text-white px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="flex space-x-1.5">
                <span className="w-3 h-3 bg-red-500 rounded-none border border-black"></span>
                <span className="w-3 h-3 bg-amber-400 rounded-none border border-black"></span>
                <span className="w-3 h-3 bg-emerald-500 rounded-none border border-black"></span>
              </div>
              <span className="font-mono text-xs font-bold tracking-wider">
                LEGACY_OS // QUANT_PORTFOLIO_NODE_09
              </span>
            </div>

            {/* Interface Tabs */}
            <div className="flex space-x-1 font-mono text-xs">
              {[
                { id: 'overview', label: '01 OVERVIEW' },
                { id: 'stress', label: '02 RISK STRESS TEST' },
                { id: 'decisions', label: '03 AI DECISION LOG' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    sound.playClick(900);
                    setActiveTab(tab.id as Tab);
                  }}
                  className={`px-3 py-1 border transition-colors ${
                    activeTab === tab.id
                      ? 'border-fintech-blue bg-fintech-blue text-white font-bold'
                      : 'border-white/20 text-white/70 hover:text-white hover:border-white'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="hidden md:flex items-center space-x-3 font-mono text-[11px] text-white/60">
              <span className="flex items-center space-x-1">
                <Lock size={12} className="text-emerald-400" />
                <span>E2E ENCRYPTED</span>
              </span>
              <Maximize2 size={13} className="cursor-pointer hover:text-white" />
            </div>
          </div>

          {/* Interface Content Area */}
          <div className="p-4 sm:p-8 bg-white">
            
            {/* Top Stat Row matching exact prompt requirements */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 pb-8 border-b-2 border-fintech-black">
              
              {/* Stat 1: Portfolio Overview */}
              <div className="border border-fintech-black p-4 bg-white shadow-brutal-sm">
                <div className="text-[10px] font-mono tracking-widest uppercase text-fintech-muted mb-1 flex items-center justify-between">
                  <span>PORTFOLIO OVERVIEW</span>
                  <span className="w-2 h-2 bg-emerald-500"></span>
                </div>
                <div className="font-display font-black text-2xl sm:text-3xl text-fintech-black">
                  {dataByTf[timeframe].total}
                </div>
                <div className="mt-1 font-mono text-[11px] text-fintech-muted flex items-center justify-between">
                  <span>AVAILABLE LIQUIDITY</span>
                  <span className="text-fintech-black font-bold">$42,800</span>
                </div>
              </div>

              {/* Stat 2: Monthly Performance */}
              <div className="border border-fintech-black p-4 bg-white shadow-brutal-sm">
                <div className="text-[10px] font-mono tracking-widest uppercase text-fintech-muted mb-1 flex items-center justify-between">
                  <span>PERFORMANCE ({timeframe})</span>
                  <span className="text-emerald-700 font-bold font-mono">+ALPHA</span>
                </div>
                <div className="font-display font-black text-2xl sm:text-3xl text-emerald-700 flex items-center">
                  {dataByTf[timeframe].change}
                </div>
                <div className="mt-1 font-mono text-[11px] text-fintech-muted flex items-center justify-between">
                  <span>BENCHMARK (SPY)</span>
                  <span className="text-fintech-black font-semibold">+4.10%</span>
                </div>
              </div>

              {/* Stat 3: AI Financial Health */}
              <div className="border border-fintech-black p-4 bg-white shadow-brutal-sm">
                <div className="text-[10px] font-mono tracking-widest uppercase text-fintech-muted mb-1 flex items-center justify-between">
                  <span>AI FINANCIAL HEALTH</span>
                  <Cpu size={14} className="text-fintech-blue" />
                </div>
                <div className="font-display font-black text-2xl sm:text-3xl text-fintech-black flex items-baseline justify-between">
                  <span>94<span className="text-lg font-mono text-fintech-muted">/100</span></span>
                  <span className="text-xs font-mono px-1.5 py-0.5 bg-fintech-blue text-white font-bold">
                    TIER 1
                  </span>
                </div>
                <div className="w-full bg-fintech-gray h-1.5 mt-2">
                  <div className="bg-fintech-blue h-full w-[94%]"></div>
                </div>
              </div>

              {/* Stat 4: Risk Exposure */}
              <div className="border border-fintech-black p-4 bg-white shadow-brutal-sm">
                <div className="text-[10px] font-mono tracking-widest uppercase text-fintech-muted mb-1 flex items-center justify-between">
                  <span>RISK EXPOSURE</span>
                  <span className="text-[10px] font-mono text-emerald-700 font-bold">SECURE</span>
                </div>
                <div className="font-display font-black text-2xl sm:text-3xl text-emerald-800 flex items-baseline justify-between">
                  <span>LOW</span>
                  <span className="text-xs font-mono text-fintech-muted font-normal">VAR: 1.1%</span>
                </div>
                <div className="mt-1 font-mono text-[11px] text-fintech-muted flex items-center justify-between">
                  <span>SHARPE RATIO</span>
                  <span className="text-fintech-black font-bold">2.84</span>
                </div>
              </div>

            </div>

            {/* Middle Section: Interactive Chart & Recommended Action Banner */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 py-8">
              
              {/* Left 8 Cols: Chart and Timeframe Controls */}
              <div className="lg:col-span-8">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
                  <div>
                    <h4 className="font-display font-bold text-lg text-fintech-black uppercase tracking-tight">
                      ALGORITHMIC VALUE TRAJECTORY
                    </h4>
                    <span className="font-mono text-xs text-fintech-muted">
                      REAL-TIME CONTINUOUS MODELING (REF: VOLATILITY-ADJUSTED)
                    </span>
                  </div>

                  {/* Timeframe Selector */}
                  <div className="flex border border-fintech-black bg-fintech-paper p-0.5 shadow-brutal-sm font-mono text-xs">
                    {(['1D', '1W', '1M', '1Y', 'ALL'] as Timeframe[]).map((tf) => (
                      <button
                        key={tf}
                        onClick={() => {
                          sound.playClick(900);
                          setTimeframe(tf);
                        }}
                        className={`px-3 py-1 font-bold transition-all ${
                          timeframe === tf
                            ? 'bg-fintech-black text-white'
                            : 'text-fintech-muted hover:text-fintech-black'
                        }`}
                      >
                        {tf}
                      </button>
                    ))}
                  </div>
                </div>

                {/* SVG Visualizer */}
                <div className="border border-fintech-black bg-fintech-paper/50 p-4 relative h-64 flex flex-col justify-end overflow-hidden">
                  <div className="absolute inset-0 bg-tech-grid-dense opacity-40 pointer-events-none"></div>

                  {/* Grid Lines */}
                  <div className="absolute inset-0 flex flex-col justify-between p-4 pointer-events-none text-[10px] font-mono text-fintech-muted/50">
                    <div className="border-b border-fintech-black/10 flex justify-between pb-1"><span>$300K</span><span>HIGH</span></div>
                    <div className="border-b border-fintech-black/10 flex justify-between pb-1"><span>$275K</span><span>MED</span></div>
                    <div className="border-b border-fintech-black/10 flex justify-between pb-1"><span>$250K</span><span>BASE</span></div>
                    <div className="flex justify-between"><span>$225K</span><span>SUPPORT</span></div>
                  </div>

                  {/* Responsive SVG Chart */}
                  <div className="relative w-full h-44 z-10">
                    <svg viewBox="0 0 480 200" className="w-full h-full overflow-visible">
                      <defs>
                        <linearGradient id="terminalGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                          <stop offset="0%" stopColor="#0052FF" stopOpacity="0.2" />
                          <stop offset="100%" stopColor="#0052FF" stopOpacity="0.0" />
                        </linearGradient>
                      </defs>

                      {/* Area */}
                      <path
                        d={`${dataByTf[timeframe].chartPath} L 480 200 L 0 200 Z`}
                        fill="url(#terminalGrad)"
                      />

                      {/* Line */}
                      <path
                        d={dataByTf[timeframe].chartPath}
                        fill="none"
                        stroke="#0052FF"
                        strokeWidth="3.5"
                        strokeLinecap="square"
                      />
                    </svg>
                  </div>

                  <div className="relative z-10 flex justify-between items-center pt-2 border-t border-fintech-black/20 font-mono text-[10px] text-fintech-muted">
                    <span>TIMEFRAME WINDOW: {timeframe}</span>
                    <span>DELTA: {dataByTf[timeframe].change}</span>
                    <span>CONFIDENCE INTERVAL: 98.7%</span>
                  </div>
                </div>
              </div>

              {/* Right 4 Cols: Exact Recommended Action Box */}
              <div className="lg:col-span-4 flex flex-col justify-between">
                <div className="border-2 border-fintech-black bg-white p-6 shadow-brutal">
                  
                  <div className="flex items-center space-x-2 text-[10px] font-mono font-bold tracking-widest text-fintech-blue uppercase mb-2">
                    <Sparkles size={14} />
                    <span>SYNTHETIC REASONING ALERT</span>
                  </div>

                  <div className="text-[11px] font-mono text-fintech-muted uppercase tracking-wider mb-1">
                    RECOMMENDED ACTION:
                  </div>

                  <h3 className="font-display font-extrabold text-xl sm:text-2xl text-fintech-black uppercase leading-tight mb-4">
                    INCREASE LONG-TERM ALLOCATION
                  </h3>

                  <p className="text-xs text-fintech-black/80 font-sans leading-relaxed mb-4">
                    Based on shifting macroeconomic rate yields and your 6-year capital horizon, reallocating 7.5% of idle cash into fixed-maturity sovereign instruments creates an estimated <strong className="text-fintech-blue">+$14,200</strong> in risk-free alpha.
                  </p>

                  <div className="border-t border-fintech-black/20 pt-3 mb-5 font-mono text-[11px] space-y-1.5 text-fintech-muted">
                    <div className="flex justify-between">
                      <span>IMPACT:</span>
                      <span className="font-bold text-fintech-black">+1.42% YIELD EFFICIENCY</span>
                    </div>
                    <div className="flex justify-between">
                      <span>DOWNSIDE DELTA:</span>
                      <span className="font-bold text-emerald-700">0.00%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>STATUS:</span>
                      <span className="font-bold text-fintech-blue">
                        {actionApplied ? 'EXECUTED // REBALANCED' : 'AWAITING YOUR APPROVAL'}
                      </span>
                    </div>
                  </div>

                  <button
                    onClick={handleApplyAction}
                    className={`w-full brutal-btn border-2 border-fintech-black py-3 font-mono text-xs font-bold uppercase tracking-wider shadow-brutal flex items-center justify-center space-x-2 cursor-pointer ${
                      actionApplied 
                        ? 'bg-emerald-600 text-white border-fintech-black' 
                        : 'bg-fintech-black text-white hover:bg-fintech-blue'
                    }`}
                  >
                    {actionApplied ? (
                      <>
                        <Check size={16} />
                        <span>REALLOCATION CONFIRMED</span>
                      </>
                    ) : (
                      <>
                        <Sliders size={16} />
                        <span>EXECUTE RECOMMENDED REBALANCE</span>
                      </>
                    )}
                  </button>

                </div>

                {/* Micro AI Prompt Simulation */}
                <div className="mt-4 border border-fintech-black bg-fintech-paper p-3 text-xs font-mono flex items-center justify-between">
                  <div className="flex items-center space-x-2 truncate mr-2">
                    <Terminal size={14} className="text-fintech-blue shrink-0" />
                    <span className="truncate text-fintech-muted">
                      &gt; prompt: &ldquo;How does inflation affect my 2030 goal?&rdquo;
                    </span>
                  </div>
                  <ChevronRight size={14} className="text-fintech-black shrink-0" />
                </div>

              </div>

            </div>

          </div>

          {/* Interface Bottom Metadata Strip */}
          <div className="border-t-2 border-fintech-black bg-fintech-paper px-6 py-2.5 flex flex-wrap justify-between items-center text-[10px] font-mono text-fintech-muted gap-2">
            <span>INTELLIGENCE HASH: 0x9F82A4...E81B</span>
            <span>DATA SOURCE: FED RESERVE + NYSE DIRECT // LATENCY 12MS</span>
            <span className="text-fintech-black font-semibold">ALGO VERIFIED: DETERMINISTIC</span>
          </div>

        </div>

      </div>
    </section>
  );
};
