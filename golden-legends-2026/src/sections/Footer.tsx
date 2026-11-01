import { Award, Heart } from 'lucide-react';

export default function Footer() {
  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText('Cookie Runners Golden Legends Awards 2026');
      alert('Title copied to clipboard!');
    } catch {
      alert('Could not copy. Try again.');
    }
  };

  return (
    <footer className="relative border-t border-white/5 bg-deep-blue/80 backdrop-blur-md py-16 md:py-20">
      <div className="max-w-6xl mx-auto px-5 md:px-8">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8 mb-10">
          <div>
            <div className="flex items-center gap-2.5 text-champagne mb-2">
              <Award className="w-5 h-5 text-gold" strokeWidth={2} />
              <span className="font-display font-bold text-base tracking-wide">Golden Legends 2026</span>
            </div>
            <p className="text-xs text-ivory/30 tracking-[0.2em] uppercase font-editorial">
              ONE KINGDOM. MANY LEGENDS. ONE COOKIE RUNNER FAMILY.
            </p>
          </div>

          <button
            onClick={handleShare}
            className="px-5 py-2.5 rounded-xl bg-white/5 border border-white/10 hover:border-gold/30 text-xs font-medium text-ivory/70 hover:text-champagne transition-all tracking-wide"
          >
            Copy Ceremony Title
          </button>
        </div>

        <div className="gold-divider mb-8" />

        {/* Disclaimer */}
        <div className="rounded-2xl bg-deep-blue-light/40 border border-white/[0.05] p-6 md:p-8 mb-8">
          <h4 className="font-display text-lg font-bold text-champagne mb-3">Unofficial Fan Project Disclaimer</h4>
          <div className="text-sm text-ivory/50 font-editorial leading-relaxed space-y-2">
            <p>
              <strong className="text-ivory/80">Cookie Runners Golden Legends Awards 2026</strong> is an unofficial, community-made fan project created by and for Cookie Runners. It is <strong>not affiliated with, endorsed by, or sponsored by</strong> Devsisters Corporation or any official Cookie Run games.
            </p>
            <p>
              All Cookie Run names, characters, artwork references, and related intellectual property belong to their respective owners. All award categories, winners, timelines, and fan creations in this site are community-made and unofficial. Nothing here represents an official announcement or product from the developers.
            </p>
            <p>
              This site uses replaceable artwork placeholders. No unauthorized artwork has been downloaded or redistributed. All content is created for celebration, learning, and community fun — with no commercial use implied or permitted for official Cookie Run intellectual property.
            </p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between gap-3 text-[11px] text-ivory/20 tracking-wide">
          <p>Every Cookie has a story. Every Cookie Runner has a memory. Every legend deserves a golden moment.</p>
          <p className="flex items-center gap-1.5">
            Built with <Heart className="w-3 h-3 text-rose-glow/60 fill-rose-glow/40" /> for the community
          </p>
        </div>
      </div>
    </footer>
  );
}
