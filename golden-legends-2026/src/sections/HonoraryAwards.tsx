import { Award, Sparkles } from 'lucide-react';
import { honoraryAwards } from '../data/awards';

export default function HonoraryAwards() {
  return (
    <section id="honorary" className="relative py-24 md:py-36">
      <div className="max-w-6xl mx-auto px-5 md:px-8">
        <div className="text-center mb-14">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-rose-glow/10 border border-rose-glow/20 text-rose-glow/80 text-xs font-medium tracking-wider uppercase mb-6">
            <Award className="w-3.5 h-3.5" /> Honorary
          </div>
          <h2 className="font-display text-4xl md:text-6xl font-bold text-ivory leading-tight mb-4">
            Honorary <span className="gold-gradient-text">Awards</span>
          </h2>
          <p className="text-ivory/50 font-editorial italic max-w-lg mx-auto">
            Beyond the main stage, some hearts shine so brightly they deserve their own golden crown.
          </p>
        </div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {honoraryAwards.map((award) => (
            <article
              key={award.id}
              className="glass-card glass-card-hover rounded-3xl p-6 md:p-7 flex flex-col transition-all duration-300 relative overflow-hidden"
            >
              {/* Subtle decorative top glow */}
              <div className="absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-gold/40 to-transparent" />

              <div className="flex items-center gap-3 mb-5">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gold/20 to-deep-blue flex items-center justify-center border border-gold/15">
                  <Sparkles className="w-5 h-5 text-gold/70" />
                </div>
                <div>
                  <h4 className="font-display text-lg font-bold text-champagne leading-snug">
                    {award.title}
                  </h4>
                  <p className="text-[10px] text-champagne-soft tracking-wider uppercase font-medium">
                    {award.subtitle}
                  </p>
                </div>
              </div>

              <h5 className="font-display text-xl font-bold text-ivory mb-2">{award.recipient}</h5>
              <p className="text-sm text-ivory/60 leading-relaxed font-editorial mb-5 flex-grow">
                {award.recognition}
              </p>

              <div className="gold-divider mb-4" />

              <div className="rounded-2xl bg-gradient-to-br from-deep-blue to-deep-blue-light border border-white/[0.05] p-4">
                <p className="text-[10px] text-ivory/30 uppercase tracking-wide mb-1">Artwork Placeholder</p>
                <p className="text-xs text-ivory/50 font-editorial italic leading-relaxed">
                  {award.artworkPlaceholder || 'Golden portrait — replace with authorized artwork.'}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
