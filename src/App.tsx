import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Mission } from './components/Mission';
import { Solutions } from './components/Solutions';
import { AIIntelligence } from './components/AIIntelligence';
import { HowItWorks } from './components/HowItWorks';
import { Security } from './components/Security';
import { CTA } from './components/CTA';
import { Footer } from './components/Footer';
import { GetStartedModal } from './components/GetStartedModal';
import { sound } from './utils/audio';

export const App: React.FC = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'onboard' | 'simulate'>('onboard');
  const [soundEnabled, setSoundEnabled] = useState(true);

  const handleOpenGetStarted = () => {
    setModalMode('onboard');
    setModalOpen(true);
  };

  const handleExplorePlatform = () => {
    setModalMode('simulate');
    setModalOpen(true);
  };

  const handleToggleSound = (): boolean => {
    const isNowEnabled = sound.toggleSound();
    setSoundEnabled(isNowEnabled);
    return isNowEnabled;
  };

  return (
    <div className="min-h-screen bg-white text-fintech-black font-sans selection:bg-fintech-blue selection:text-white">
      {/* Sticky Institutional Navbar */}
      <Navbar 
        onOpenGetStarted={handleOpenGetStarted}
        soundEnabled={soundEnabled}
        onToggleSound={handleToggleSound}
      />

      <main id="main-content">
        {/* Section 01: Hero Split-Screen with Editorial Headline & Fintech Visual */}
        <Hero 
          onOpenGetStarted={handleOpenGetStarted}
          onExplorePlatform={handleExplorePlatform}
          soundEnabled={soundEnabled}
          onToggleSound={handleToggleSound}
        />

        {/* Section 02: Mission - Finance Should Work For You */}
        <Mission />

        {/* Section 03: Solutions - One Intelligent Financial Ecosystem */}
        <Solutions />

        {/* Section 04: AI Financial Intelligence Interface */}
        <AIIntelligence />

        {/* Section 05: How It Works - From Data to Decision */}
        <HowItWorks />

        {/* Section 06: Trust & Security - Your Finances. Your Control */}
        <Security />

        {/* Section 07: Call to Action - Build a Smarter Financial Future */}
        <CTA onOpenGetStarted={handleOpenGetStarted} />
      </main>

      {/* Structured Institutional Footer */}
      <Footer />

      {/* Interactive Modal */}
      <GetStartedModal 
        isOpen={modalOpen} 
        onClose={() => setModalOpen(false)} 
        initialMode={modalMode}
      />
    </div>
  );
};

export default App;
