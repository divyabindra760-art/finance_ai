import React, { useState } from 'react';
import { TrendingUp, ShieldCheck, Activity, Brain, ArrowUpRight, Zap, RefreshCw } from 'lucide-react';
import { sound } from '../utils/audio';

export const HeroVisual: React.FC = () => {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);
  const [activeRange, setActiveRange] = useState<'Q1' | 'Q2' | 'Q3' | 'Q4' | 'MAX'>('MAX');
  const [isSimulating, setIsSimulating] = useState(false);

  // SVG Chart points
  const points = [
    { x: 20, y: 190, val: '$1.42M', date: '2022' },
    { x: 90, y: 175, val: '$1.68M', date: '2023' },
    { x: 160, y: 155, val: '$1.95M', date: '2024' },
    { x: 230, y: 120, val: '$2.30M', date: '2025' },
    { x: 300, y: 85, val: '$2.58M', date: '2026' },
    { x: 380, y: 45, val: '$2.84M', date: '2026 Q3' },
    { x: 440, y: 22, val: '$3.25M', date: '2027 (PROJ)' },
  ];

  const handleSimulate = () => {
    sound.playClick(1100);
    setIsSimulating(true);
    setTimeout(() => {
      sound.playChime();
      setIsSimulating(false);
    }, 600);
  };

  return (
    <div className="relative w-full max-w-xl mx-auto lg:max-w-none">
      {/* Outer Rectangular Container with Double Border & Offset Shadow */}
      <div className="relative border-[3px] border-fintech-black bg-white shadow-brutal-xl p-3 sm:p-5 transition-all duration-300">
        
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

        {/* Inner Thin Border Container */}
        <div className="border border-fintech-black/40 p-4 sm:p-6 bg-white relative overflow-hidden">
          
          {/* Subtle grid background inside visual */}
          <div className="absolute inset-0 bg-tech-grid-dense opacity-60 pointer-events-none"></div>

          {/* Technical Header inside visual */}
          <div className="relative z-10 flex flex-wrap justify-between items-center pb-3 border-b border-fintech-black/20 gap-2">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-fintech-blue animate-pulse"></div>
              <span className="text-xs font-mono font-bold tracking-wider text-fintech-black">
                TERMINAL // CORE_ENGINE.AI
              </span>
            </div>
            <div className="flex items-center space-x-2 text-[10px] font-mono text-fintech-muted">
              <span>MODEL: NEURAL_L5</span>
              <span>•</span>
              <span className="text-emerald-700 font-semibold">OPTIMIZED</span>
              <button
                onClick={handleSimulate}
                title="Rerun AI Optimization Simulation"
                className="p-1 border border-fintech-black/30 hover:border-fintech-black hover:bg-fintech-paper transition-colors"
              >
                <RefreshCw size={11} className={isSimulating ? 'animate-spin text-fintech-blue' : ''} />
              </button>
            </div>
          </div>

          {/* Floating Data Card 1: Main Portfolio Value */}
          <div className="relative z-10 my-4 flex flex-wrap items-baseline justify-between gap-4">
            <div>
              <div className="text-[11px] font-mono uppercase tracking-widest text-fintech-muted flex items-center space-x-1.5">
                <span>PORTFOLIO VALUE</span>
                <span className="inline-block px-1.5 py-0.2 text-[9px] bg-fintech-paper border border-fintech-black/30 text-fintech-black font-semibold">
                  LIVE
                </span>
              </div>
              <div className="font-display font-extrabold text-3xl sm:text-4xl lg:text-5xl text-fintech-black tracking-tight mt-1">
                {isSimulating ? (
                  <span className="animate-pulse text-fintech-blue">$2,842,910</span>
                ) : (
                  '$2,840,450'
                )}
              </div>
            </div>

            {/* Annual Growth Badge */}
            <div className="border border-fintech-black bg-white p-2.5 shadow-brutal-sm flex items-center space-x-3">
              <div className="w-7 h-7 bg-fintech-black text-white flex items-center justify-center">
                <TrendingUp size={16} className="text-emerald-400" />
              </div>
              <div>
                <div className="text-[9px] font-mono uppercase text-fintech-muted">ANNUAL GROWTH</div>
                <div className="text-sm font-mono font-bold text-fintech-black flex items-center text-emerald-800">
                  +18.7%
                  <span className="text-[10px] ml-1 font-normal text-fintech-muted">vs S&P (+11.2%)</span>
                </div>
              </div>
            </div>
          </div>

          {/* Interactive Visual Graph Canvas */}
          <div className="relative z-10 my-4 bg-fintech-paper/80 border border-fintech-black/30 p-3">
            {/* Range Pills */}
            <div className="flex justify-between items-center mb-2">
              <div className="text-[10px] font-mono uppercase text-fintech-muted flex items-center space-x-1">
                <Activity size={12} className="text-fintech-blue" />
                <span>DYNAMIC YIELD CURVE</span>
              </div>
              <div className="flex space-x-1 font-mono text-[10px]">
                {(['Q1', 'Q2', 'Q3', 'Q4', 'MAX'] as const).map((r) => (
                  <button
                    key={r}
                    onClick={() => {
                      sound.playClick(950);
                      setActiveRange(r);
                    }}
                    className={`px-1.5 py-0.5 border ${
                      activeRange === r 
                        ? 'border-fintech-black bg-fintech-black text-white font-bold' 
                        : 'border-transparent text-fintech-muted hover:text-fintech-black'
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </div>

            {/* SVG Chart */}
            <div className="relative w-full h-44">
              <svg 
                viewBox="0 0 460 210" 
                className="w-full h-full overflow-visible"
              >
                <defs>
                  <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#08090C" />
                    <stop offset="70%" stopColor="#0052FF" />
                    <stop offset="100%" stopColor="#0052FF" />
                  </linearGradient>
                  <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#0052FF" stopOpacity="0.15" />
                    <stop offset="100%" stopColor="#0052FF" stopOpacity="0.00" />
                  </linearGradient>
                </defs>

                {/* Horizontal reference grid lines */}
                <line x1="10" y1="50" x2="450" y2="50" stroke="#08090C" strokeOpacity="0.1" strokeDasharray="3 3" />
                <line x1="10" y1="100" x2="450" y2="100" stroke="#08090C" strokeOpacity="0.1" strokeDasharray="3 3" />
                <line x1="10" y1="150" x2="450" y2="150" stroke="#08090C" strokeOpacity="0.1" strokeDasharray="3 3" />

                {/* Area Fill */}
                <path
                  d="M 20 190 L 90 175 L 160 155 L 230 120 L 300 85 L 380 45 L 440 22 L 440 200 L 20 200 Z"
                  fill="url(#areaGrad)"
                />

                {/* Main Curve */}
                <path
                  d="M 20 190 L 90 175 L 160 155 L 230 120 L 300 85 L 380 45 L 440 22"
                  fill="none"
                  stroke="url(#lineGrad)"
                  strokeWidth="3"
                  strokeLinecap="square"
                />

                {/* Projection dashed segment */}
                <line 
                  x1="380" y1="45" x2="440" y2="22" 
                  stroke="#0052FF" 
                  strokeWidth="2.5" 
                  strokeDasharray="4 3" 
                />

                {/* Interactive Points */}
                {points.map((pt, idx) => (
                  <g 
                    key={idx} 
                    className="cursor-pointer"
                    onMouseEnter={() => {
                      sound.playClick(1000 + idx * 60);
                      setHoverIndex(idx);
                    }}
                    onMouseLeave={() => setHoverIndex(null)}
                  >
                    <rect
                      x={pt.x - 4}
                      y={pt.y - 4}
                      width="8"
                      height="8"
                      fill={idx === points.length - 2 ? '#0052FF' : '#08090C'}
                      stroke="#FFFFFF"
                      strokeWidth="1.5"
                      className="transition-transform hover:scale-150"
                    />
                  </g>
                ))}
              </svg>

              {/* Hover Tooltip */}
              {hoverIndex !== null && (
                <div 
                  className="absolute z-30 bg-fintech-black text-white p-2 text-[10px] font-mono shadow-brutal pointer-events-none border border-white/20"
                  style={{ 
                    left: `${(points[hoverIndex].x / 460) * 85}%`, 
                    top: `${points[hoverIndex].y - 35}px` 
                  }}
                >
                  <div className="text-fintech-blue font-bold">{points[hoverIndex].val}</div>
                  <div className="text-white/70">{points[hoverIndex].date}</div>
                </div>
              )}
            </div>
          </div>

          {/* Floating Data Micro-Cards: AI SCORE, RISK, PROJECTED 2030 */}
          <div className="relative z-10 grid grid-cols-3 gap-2.5 pt-2">
            
            {/* Card 1: AI SCORE */}
            <div className="border border-fintech-black p-2.5 bg-white shadow-brutal-sm">
              <div className="flex items-center justify-between text-[9px] font-mono text-fintech-muted uppercase mb-1">
                <span>AI SCORE</span>
                <Brain size={12} className="text-fintech-blue" />
              </div>
              <div className="text-lg sm:text-xl font-display font-extrabold text-fintech-black flex items-baseline justify-between">
                <span>94.8</span>
                <span className="text-[9px] font-mono text-emerald-600 font-semibold">AAA</span>
              </div>
              <div className="w-full bg-fintech-gray h-1 mt-1.5 overflow-hidden">
                <div className="bg-fintech-blue h-full w-[94.8%]"></div>
              </div>
            </div>

            {/* Card 2: RISK */}
            <div className="border border-fintech-black p-2.5 bg-white shadow-brutal-sm">
              <div className="flex items-center justify-between text-[9px] font-mono text-fintech-muted uppercase mb-1">
                <span>RISK LEVEL</span>
                <ShieldCheck size={12} className="text-emerald-700" />
              </div>
              <div className="text-lg sm:text-xl font-display font-extrabold text-emerald-800 flex items-baseline justify-between">
                <span>LOW</span>
                <span className="text-[9px] font-mono text-fintech-muted">β: 0.62</span>
              </div>
              <div className="text-[9px] font-mono text-fintech-muted mt-1">
                HEDGED ALPHA
              </div>
            </div>

            {/* Card 3: PROJECTED 2030 */}
            <div className="border border-fintech-black p-2.5 bg-white shadow-brutal-sm">
              <div className="flex items-center justify-between text-[9px] font-mono text-fintech-muted uppercase mb-1">
                <span>PROJECTED</span>
                <Zap size={12} className="text-amber-600" />
              </div>
              <div className="text-lg sm:text-xl font-display font-extrabold text-fintech-black flex items-baseline justify-between">
                <span>2030</span>
                <span className="text-[9px] font-mono text-fintech-blue font-semibold">$4.9M</span>
              </div>
              <div className="text-[9px] font-mono text-fintech-muted mt-1">
                EST. RETURN
              </div>
            </div>

          </div>

          {/* Micro Asset Allocation Strip */}
          <div className="relative z-10 mt-3 pt-3 border-t border-fintech-black/10 flex items-center justify-between text-[9px] font-mono">
            <span className="text-fintech-muted">ALLOCATION:</span>
            <div className="flex items-center space-x-2">
              <span className="flex items-center"><span className="w-1.5 h-1.5 bg-fintech-black inline-block mr-1"></span>EQ 58%</span>
              <span className="flex items-center"><span className="w-1.5 h-1.5 bg-fintech-blue inline-block mr-1"></span>FI 22%</span>
              <span className="flex items-center"><span className="w-1.5 h-1.5 bg-slate-400 inline-block mr-1"></span>ALT 14%</span>
              <span className="flex items-center"><span className="w-1.5 h-1.5 bg-emerald-500 inline-block mr-1"></span>CSH 6%</span>
            </div>
            <div className="flex items-center text-fintech-blue font-semibold hover:underline cursor-pointer" onClick={() => sound.playClick()}>
              <span>DETAILS</span>
              <ArrowUpRight size={10} />
            </div>
          </div>

        </div>
      </div>

      {/* Decorative Technical Label Outside Box */}
      <div className="mt-2 flex justify-between items-center text-[10px] font-mono text-fintech-muted px-1">
        <span>FIG. 01 — MULTI-DIMENSIONAL ASSET ORCHESTRATION</span>
        <span>LAT: 40.7128° N, 74.0060° W</span>
      </div>
    </div>
  );
};
