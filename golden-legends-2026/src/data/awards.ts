export interface Winner {
  id: string;
  name: string;
  role: string;
  recognition: string;
  artworkPlaceholder: string;
}

export interface AwardCategory {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  winner: Winner;
  isHonorary?: boolean;
  tag?: string;
}

export interface HonoraryAward {
  id: string;
  title: string;
  subtitle: string;
  recipient: string;
  recognition: string;
  artworkPlaceholder?: string;
}

export const mainAwards: AwardCategory[] = [
  {
    id: "legend-kingdom",
    title: "LEGEND OF COOKIE RUN KINGDOM",
    subtitle: "The Crown of Memory",
    description:
      "Her unforgettable legacy, courage, and story shaped the kingdom forever. A light that continues to guide every Cookie Runner.",
    winner: {
      id: "white-lily",
      name: "White Lily Cookie",
      role: "Legend of Cookie Run Kingdom",
      recognition:
        "Unforgettable legacy, courage, and story that transformed the kingdom and inspired generations of Cookie Runners.",
      artworkPlaceholder: "White Lily portrait — gentle silver-white hair, floral crown, soft gold aura.",
    },
    tag: "Main Award",
  },
  {
    id: "best-double-update",
    title: "BEST DOUBLE UPDATE",
    subtitle: "Two Worlds, One Celebration",
    description:
      "Two exciting worlds arrived together, doubling the magic for every player and proving that great stories come in pairs.",
    winner: {
      id: "double-update",
      name: "Cradle for the Sleepless Dragon × The Amazing Digital Circus",
      role: "Best Double Update",
      recognition:
        "Two exciting worlds in one celebration — a fresh gameplay experience and a digital spectacle that redefined the year.",
      artworkPlaceholder: "Cradle dragon artwork and Digital Circus stage scene — paired golden frames.",
    },
    tag: "Main Award",
  },
  {
    id: "best-original-game",
    title: "BEST ORIGINAL COOKIE RUN GAME",
    subtitle: "A Fresh Start",
    description:
      "A bold new entry that expanded the universe and reminded every Cookie Runner why the journey is always worth it.",
    winner: {
      id: "oven-smash",
      name: "CookieRun: OvenSmash",
      role: "Best Original Cookie Run Game",
      recognition:
        "A fresh gameplay experience in the Cookie Run universe — innovative mechanics, welcoming design, and pure fun.",
      artworkPlaceholder: "OvenSmash key art — oven flames, cookie heroes, golden sparks.",
    },
    tag: "Main Award",
  },
];

export const honoraryAwards: HonoraryAward[] = [
  {
    id: "golden-heart",
    title: "Golden Heart Award",
    subtitle: "For Kindness Beyond Measure",
    recipient: "Pure Vanilla Cookie",
    recognition:
      "A heart that heals, guides, and reminds the kingdom that gentleness is the greatest strength of all.",
    artworkPlaceholder:
      "Pure Vanilla portrait — soft golden hair, pearl-white robes, warm glowing light.",
  },
  {
    id: "golden-teammate",
    title: "Golden Teammate Award",
    subtitle: "The Heart of Every Team",
    recipient: "Pure Vanilla Cookie",
    recognition:
      "Always there for every Cookie, every battle, every quiet moment in between. The teammate legends are made of.",
    artworkPlaceholder:
      "Pure Vanilla portrait — gentle smile, outstretched hand, warm golden glow.",
  },
  {
    id: "legendary-duo",
    title: "Legendary Duo Award",
    subtitle: "Pure Lily",
    recipient: "White Lily Cookie + Pure Vanilla Cookie",
    recognition:
      "Two souls whose light shines brighter together. A legend of friendship, loyalty, and eternal hope.",
    artworkPlaceholder:
      "White Lily and Pure Vanilla side by side — silver and gold light intertwined.",
  },
  {
    id: "eternal-flame",
    title: "Eternal Flame Award",
    subtitle: "For Burning Bright Forever",
    recipient: "Burning Spice Cookie & Mogra Cookie",
    recognition:
      "Their fire never fades. Their warmth reaches every corner of the kingdom and beyond.",
    artworkPlaceholder:
      "Burning Spice and Mogra — twin flames, crimson and amber, golden sparks.",
  },
  {
    id: "fan-community",
    title: "Fan Community Award",
    subtitle: "Built by Cookie Runners",
    recipient: "Cookie Runners",
    recognition:
      "Every celebration, every memory, every golden moment is made possible by the community that never stops believing.",
    artworkPlaceholder:
      "Cookie Runners community banner — golden cookies, shared smiles, warm light.",
  },
  {
    id: "gaming-journey",
    title: "Best Gaming Journey",
    subtitle: "From K-pop to Kingdom",
    recipient: "From K-pop Demon Hunters to Cookie Run",
    recognition:
      "A journey across worlds, from stage lights to kingdom gates — proof that passion connects everything.",
    artworkPlaceholder:
      "Journey collage — stage lights, cookie kingdom gates, golden path.",
  },
];

export interface TimelineEvent {
  date: string;
  title: string;
  description: string;
}

export const timelineEvents: TimelineEvent[] = [
  { date: "March 11, 2026", title: "White Lily Remembrance", description: "A solemn tribute to White Lily Cookie's enduring legacy." },
  { date: "December 8, 2025", title: "Salute Night Ceremony", description: "The community honored the heroes of the kingdom together." },
  { date: "October 31, 2026", title: "First Golden Legends Edition", description: "The very first Cookie Runners Golden Legends Awards — ONE KINGDOM. MANY LEGENDS." },
];
