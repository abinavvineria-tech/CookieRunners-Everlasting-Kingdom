import { Heart, Sparkles, Users } from 'lucide-react';

export default function About() {
  return (
    <section id="about" className="relative py-24 md:py-36">
      <div className="max-w-5xl mx-auto px-5 md:px-8">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16 items-start">
          {/* Left: Community story */}
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-champagne/10 border border-champagne/20 text-champagne text-xs font-medium tracking-wider uppercase mb-6">
              <Users className="w-3.5 h-3.5" /> Community
            </div>
            <h2 className="font-display text-4xl md:text-5xl font-bold text-ivory leading-tight mb-6">
              About Cookie <span className="gold-gradient-text">Runners</span>
            </h2>
            <div className="space-y-4 text-ivory/60 font-editorial leading-relaxed text-base">
              <p>
                This is an <strong className="text-champagne-soft font-medium">unofficial fan project</strong> created for the Cookie Runners community — the people who keep the kingdom alive with every celebration, every memory, and every shared smile.
              </p>
              <p>
                The Golden Legends Awards 2026 is the <strong className="text-champagne-soft font-medium">first edition</strong> of a ceremony dedicated to honoring the characters, stories, and community moments that define the Cookie Run experience for players everywhere.
              </p>
              <p>
                No official endorsement. No commercial intent. Just a golden celebration made by Cookie Runners, for Cookie Runners.
              </p>
            </div>
          </div>

          {/* Right: Values / identity */}
          <div className="glass-card rounded-3xl p-8 md:p-10 border-gold/15 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-gradient-to-br from-gold/10 to-transparent rounded-full -translate-y-1/2 translate-x-1/4" />

            <h3 className="font-display text-2xl font-bold text-champagne mb-8 relative">
              Our Identity
            </h3>

            <div className="space-y-6 relative">
              <div className="flex gap-4">
                <div className="w-9 h-9 rounded-xl bg-gold/10 border border-gold/20 flex items-center justify-center shrink-0">
                  <Heart className="w-4 h-4 text-gold" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-ivory mb-1">Respect for the Original</h4>
                  <p className="text-sm text-ivory/50 font-editorial leading-relaxed">
                    Every character, name, and story belongs to its creators. We celebrate without claiming ownership.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-9 h-9 rounded-xl bg-champagne/10 border border-champagne/20 flex items-center justify-center shrink-0">
                  <Sparkles className="w-4 h-4 text-champagne" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-ivory mb-1">Fan-First Design</h4>
                  <p className="text-sm text-ivory/50 font-editorial leading-relaxed">
                    This site is built for mobile, tested on real devices, and designed to feel like a true ceremony.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="w-9 h-9 rounded-xl bg-violet-soft/10 border border-violet-soft/20 flex items-center justify-center shrink-0">
                  <Users className="w-4 h-4 text-violet-soft" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-ivory mb-1">Community Together</h4>
                  <p className="text-sm text-ivory/50 font-editorial leading-relaxed">
                    ONE KINGDOM. MANY LEGENDS. ONE COOKIE RUNNER FAMILY. The motto is the mission.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
