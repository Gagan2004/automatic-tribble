import React from 'react';
import { ExternalLink, Star, Zap } from 'lucide-react';

const RecommendationCard = ({ item, isArabic }) => {
  return (
    <div className="group relative">
      {/* Dynamic Glow Background */}
      <div className="absolute -inset-0.5 bg-gradient-to-br from-violet-600/20 to-fuchsia-600/20 rounded-[2.5rem] blur-2xl opacity-0 group-hover:opacity-100 transition duration-700"></div>

      <div className="relative recommendation-card h-full flex flex-col p-8 md:p-10 border border-white/5 bg-white/[0.03] backdrop-blur-3xl hover:border-white/10 transition-all duration-700">

        {/* Card Header: Badge & Price */}
        <div className="flex justify-between items-start mb-8">
          <div className="flex items-center gap-2 px-3.5 py-1.5 bg-violet-600/10 border border-violet-500/20 rounded-xl text-[10px] font-black text-violet-400 uppercase tracking-widest shadow-2xl">
            <Zap className="w-3 h-3 fill-violet-400" />
            AI Selection
          </div>
          <div className="text-right">
            <div className="flex items-baseline gap-1">
              <span className="text-3xl font-black text-white tracking-tighter">
                {item.price}
              </span>
              <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">AED</span>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="flex-grow space-y-6">
          <div>
            <h3 className="text-2xl font-outfit font-black text-white leading-[1.1] group-hover:text-violet-400 transition-colors duration-500">
              {item.name}
            </h3>
            <div className="flex items-center gap-1 mt-3">
              {[1, 2, 3, 4, 5].map(i => (
                <Star key={i} className="w-3 h-3 fill-amber-400/80 text-amber-400/80" />
              ))}
              {/* <span className="text-[10px] font-black text-slate-500 ml-2 uppercase tracking-widest">Verified Quality</span> */}
            </div>
          </div>

          <div className="w-12 h-1 bg-gradient-to-r from-violet-600 to-transparent rounded-full opacity-40" />

          <div className={`${isArabic ? 'text-right' : 'text-left'}`}>
            <p className={`text-slate-400 leading-relaxed tracking-wide ${isArabic ? 'font-arabic text-xl leading-relaxed' : 'text-sm font-medium'}`}>
              {isArabic ? item.reason_ar : item.reason_en}
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="mt-10">
          <button className="w-full py-4 rounded-[1.25rem] bg-white/5 border border-white/5 text-white font-black text-[11px] tracking-[0.15em] flex items-center justify-center gap-3 hover:bg-violet-600 hover:border-violet-600 transition-all duration-500 active:scale-[0.98] shadow-xl group-hover:shadow-violet-600/10">
            {isArabic ? 'استكشاف المنتج' : 'EXPLORE MATCH'}
            <ExternalLink className="w-3.5 h-3.5 group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default RecommendationCard;
