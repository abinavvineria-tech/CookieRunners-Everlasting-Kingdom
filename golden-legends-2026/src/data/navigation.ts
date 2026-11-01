export interface NavLink {
  label: string;
  href: string;
  sectionId: string;
}

export const navLinks: NavLink[] = [
  { label: "Ceremony", href: "#ceremony", sectionId: "ceremony" },
  { label: "Awards", href: "#awards", sectionId: "awards" },
  { label: "Honorary", href: "#honorary", sectionId: "honorary" },
  { label: "Timeline", href: "#timeline", sectionId: "timeline" },
  { label: "About", href: "#about", sectionId: "about" },
];
