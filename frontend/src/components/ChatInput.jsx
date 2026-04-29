import React, { useState } from 'react';
import { Search, ArrowRight, Loader2, Sparkles } from 'lucide-react';

const ChatInput = ({ onSend, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSend(query);
      setQuery('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="relative w-full flex items-center group">
      {/* Icon Section */}
      <div className="absolute left-6 pointer-events-none">
        {isLoading ? (
          <Sparkles className="w-6 h-6 text-violet-400 animate-pulse fill-violet-400/20" />
        ) : (
          <Search className="w-6 h-6 text-slate-500 group-focus-within:text-violet-400 transition-colors" />
        )}
      </div>
      
      {/* Input Field */}
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={isLoading ? "Mama AI is thinking..." : "Try 'organic baby food for 7 months'..."}
        className="w-full pl-16 pr-32 py-6 text-xl bg-transparent font-outfit font-bold focus:outline-none placeholder:text-slate-600 text-white transition-all caret-violet-500"
        disabled={isLoading}
      />

      {/* Submit Button */}
      <div className="absolute right-3">
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className={`px-8 py-3.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all flex items-center gap-2 shadow-2xl ${
            isLoading || !query.trim() 
            ? 'bg-white/5 text-slate-600 opacity-50 cursor-not-allowed' 
            : 'bg-violet-600 text-white hover:bg-violet-500 hover:shadow-violet-600/30 active:scale-95'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Matching</span>
            </div>
          ) : (
            <>
              Search
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </>
          )}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
