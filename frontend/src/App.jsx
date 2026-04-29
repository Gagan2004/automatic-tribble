import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sparkles, Heart, Loader2, RefreshCw, AlertCircle, Search as SearchIcon } from 'lucide-react';
import ChatInput from './components/ChatInput';
import RecommendationCard from './components/RecommendationCard';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [progressStage, setProgressStage] = useState(0);
  const [isArabic, setIsArabic] = useState(false);
  const [error, setError] = useState(null);
  const [lastQuery, setLastQuery] = useState("");
  const [isRefining, setIsRefining] = useState(false);

  const stages = [
    { id: 1, text: "Understanding query...", textAr: "فهم الاستفسار..." },
    { id: 2, text: "Searching catalog...", textAr: "البحث في الكتالوج..." },
    { id: 3, text: "AI Reasoning...", textAr: "تحليل الذكاء الاصطناعي..." }
  ];

  const handleSend = async (query) => {
    setIsLoading(true);
    setIsRefining(false);
    setProgressStage(1);
    setError(null);
    setLastQuery(query);
    setRecommendations([]);

    const stageTimer = setInterval(() => {
      setProgressStage(prev => (prev < 3 ? prev + 1 : prev));
    }, 1500);

    try {
      const response = await axios.post(`${API_BASE_URL}/recommend`, { query });
      setRecommendations(response.data.recommendations);
      setProgressStage(0);
    } catch (err) {
      setError('Service is currently busy. Please try again in a moment.');
      setProgressStage(0);
    } finally {
      clearInterval(stageTimer);
      setIsLoading(false);
    }
  };

  const hasResults = recommendations.length > 0;
  const isMinimized = hasResults && !isRefining;

  return (
    <div className={`h-screen w-screen flex flex-col bg-[#050505] text-white selection:bg-violet-500/30 ${isArabic ? 'rtl font-arabic' : 'ltr font-sans'}`} dir={isArabic ? 'rtl' : 'ltr'}>
      
      {/* Background Glows */}
      <div className="fixed inset-0 pointer-events-none -z-10">
        <div className="absolute top-[-10%] right-[-10%] w-[50vw] h-[50vw] bg-violet-600/10 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-[-10%] left-[-10%] w-[50vw] h-[50vw] bg-fuchsia-600/5 rounded-full blur-[120px] animate-pulse"></div>
      </div>

      {/* Dynamic Header / Navbar Replacement */}
      <header className={`flex-none px-8 py-5 flex justify-between items-center border-b border-white/5 bg-black/40 backdrop-blur-xl z-50 transition-all duration-700 ${isMinimized ? 'opacity-0 -translate-y-full pointer-events-none' : 'opacity-100 translate-y-0'}`}>
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-violet-600/20">
            <Heart className="text-white w-5 h-5 fill-white" />
          </div>
          <span className="text-xl font-outfit font-black tracking-tighter">
            Mama<span className="text-violet-400">AI</span>
          </span>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex bg-white/5 p-1 rounded-xl border border-white/10">
            <button 
              onClick={() => setIsArabic(false)}
              className={`px-3 py-1 rounded-lg text-[10px] font-bold transition-all ${!isArabic ? 'bg-violet-600 text-white' : 'text-slate-400'}`}
            >EN</button>
            <button 
              onClick={() => setIsArabic(true)}
              className={`px-3 py-1 rounded-lg text-[10px] font-bold transition-all ${isArabic ? 'bg-violet-600 text-white' : 'text-slate-400'}`}
            >AR</button>
          </div>
        </div>
      </header>

      <main className="flex-grow flex flex-col min-h-0 relative px-6 overflow-hidden">
        
        {/* ADAPTIVE SEARCH BOX */}
        <div 
          className={`fixed left-1/2 -translate-x-1/2 z-[60] transition-all duration-700 ease-in-out cursor-pointer group ${
            isMinimized 
            ? 'top-4 w-[600px] scale-75 opacity-100' 
            : 'top-[30vh] w-full max-w-4xl scale-100'
          } ${recommendations.length > 0 && !isMinimized ? 'top-10' : ''}`}
          onClick={() => isMinimized && setIsRefining(true)}
        >
          {!hasResults && !isLoading && !isRefining && (
            <div className="text-center mb-10 space-y-4 animate-in fade-in duration-1000">
              <h1 className="text-5xl md:text-7xl font-outfit font-black tracking-tight leading-none">
                Parenting <span className="gradient-text">Genius</span>.
              </h1>
              <p className="text-slate-400 text-lg">Curated matches for your child's milestones.</p>
            </div>
          )}
          
          <div className={`relative glass-card !bg-white/5 !p-2 transition-all duration-500 ${isMinimized ? 'hover:!bg-white/10 border-violet-500/30' : ''}`}>
            {isMinimized && (
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/40 backdrop-blur-sm rounded-[2rem] z-10">
                <div className="flex items-center gap-2 text-xs font-black uppercase tracking-widest text-violet-400">
                  <RefreshCw className="w-4 h-4" />
                  Click to refine search
                </div>
              </div>
            )}
            <ChatInput onSend={handleSend} isLoading={isLoading} />
          </div>

          {!hasResults && !isLoading && !isRefining && (
            <div className="flex flex-wrap justify-center gap-2 mt-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-300">
              {["11 month old can't sleep", "Baby has eating problems", "Safe toys for teething", "Help with diaper rash"].map(tag => (
                <button key={tag} onClick={(e) => { e.stopPropagation(); handleSend(tag); }} className="px-4 py-1.5 bg-white/5 border border-white/5 rounded-full text-[10px] font-bold text-slate-400 hover:text-white transition-all">
                  {tag}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Results / Loading Area */}
        <div className={`flex-grow overflow-hidden flex flex-col transition-all duration-700 ${hasResults || isLoading ? 'mt-32' : 'mt-0'}`}>
          {isLoading && (
            <div className="flex flex-col items-center justify-center py-12 space-y-4 animate-in fade-in zoom-in duration-500">
              <Loader2 className="w-10 h-10 text-violet-500 animate-spin" />
              <div className="text-sm font-bold text-violet-300 tracking-widest uppercase">
                {isArabic ? stages[progressStage-1]?.textAr : stages[progressStage-1]?.text}
              </div>
            </div>
          )}

          {error && (
            <div className="max-w-md mx-auto p-4 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-3 text-red-400 text-sm font-medium mb-8">
              <AlertCircle className="w-5 h-5" />
              <span>{error}</span>
            </div>
          )}

          <div className="flex-grow overflow-y-auto pb-20 custom-scrollbar">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {recommendations.map((item, i) => (
                <div key={item.id} className="animate-in fade-in slide-in-from-bottom-8 duration-700" style={{ animationDelay: `${i * 100}ms` }}>
                  <RecommendationCard item={item} isArabic={isArabic} />
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>

      {/* Minimal Footer */}
      <footer className="flex-none py-3 px-8 flex justify-between items-center text-[9px] text-slate-600 font-bold uppercase tracking-widest bg-black/60 border-t border-white/5 z-[70]">
        <div>© 2026 MamaAI • Intelligent Parenting</div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-1.5">
            <div className="w-1 h-1 bg-green-500 rounded-full" />
            System Active
          </span>
        </div>
      </footer>
    </div>
  );
}

export default App;
