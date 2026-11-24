import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Package, Search, RefreshCw } from "lucide-react";
import { api } from "@/lib/api";

type Skill = {
  name: string;
  category: string;
  description: string;
  loaded: boolean;
};

const DEFAULT_SKILLS: Skill[] = [
  { name: "cookie-run-intelligence", category: "Cookie Run", description: "Cookie Run Kingdom intelligence: updates, Cookies, costumes", loaded: true },
  { name: "cru-management", category: "CRU Club", description: "Cookie Runners United fictional club management", loaded: true },
  { name: "hermes-agent-engineer", category: "Hermes", description: "Hermes Agent architecture, profile management", loaded: true },
  { name: "telegram-bot-engineer", category: "Automation", description: "Telegram bot design, commands and responses", loaded: true },
  { name: "termux-linux-engineer", category: "System", description: "Android 14 and Termux support: Zsh, Linux, Ubuntu", loaded: true },
  { name: "creative-studio", category: "Creative", description: "Announcements, project descriptions, matchday posts", loaded: true },
  { name: "research-intelligence", category: "Research", description: "Trustworthy source research, information comparison", loaded: true },
  { name: "matchday-intelligence", category: "Football", description: "Upcoming match discovery, daily/weekly schedules", loaded: true },
  { name: "football-intelligence", category: "Football", description: "Real-world football research: leagues, clubs, fixtures", loaded: true },
  { name: "automation-manager", category: "Automation", description: "Scheduled tasks, recurring reports, reminders", loaded: true },
];

export default function StudioSkillsPage() {
  const [skills, setSkills] = useState<Skill[]>(DEFAULT_SKILLS);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);

  const loadSkills = async () => {
    setLoading(true);
    try {
      const resp = await api.getSkills?.().catch(() => ({ skills: [] }));
      const fetched = (resp as any)?.skills;
      if (Array.isArray(fetched)) {
        setSkills(fetched.map((s: any) => ({
          name: s.name,
          category: s.category ?? "General",
          description: s.description ?? "",
          loaded: s.loaded ?? true,
        })));
      }
    } catch { /* keep defaults */ }
    setLoading(false);
  };

  const toggleSkill = (name: string) => {
    setSkills(skills.map((s) =>
      s.name === name ? { ...s, loaded: !s.loaded } : s
    ));
  };

  const filtered = skills.filter((s) =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.category.toLowerCase().includes(search.toLowerCase()) ||
    s.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Skills Lab
          </h1>
          <p className="text-muted-foreground">
            Inspect and manage Everlily Nexus agent skills
          </p>
        </div>
        <Button onClick={loadSkills} className="flex items-center gap-2">
          <RefreshCw className="h-4 w-4" /> Refresh
        </Button>
      </div>

      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <input
          className="h-10 pl-9 pr-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          placeholder="Search skills…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {loading ? (
          <div className="col-span-3 flex flex-col items-center justify-center py-12">
            <div className="h-6 w-6 rounded-full border-4 border-primary border-t-transparent animate-spin" />
            <p className="mt-2 text-muted-foreground">Loading skills…</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="col-span-3 flex flex-col items-center justify-center py-12">
            <Package className="h-12 w-12 text-muted-foreground mb-3" />
            <p className="text-muted-foreground">No skills found matching your search.</p>
          </div>
        ) : (
          filtered.map((skill) => (
            <Card key={skill.name} className="flex flex-col">
              <CardHeader className="flex flex-row items-center justify-between">
                <div className="flex items-center gap-2">
                  <Package className="h-4 w-4 text-muted-foreground" />
                  <CardTitle className="text-sm font-semibold text-foreground">{skill.name}</CardTitle>
                </div>
                <Badge variant={skill.loaded ? "default" : "secondary"}>
                  {skill.loaded ? "Loaded" : "Unloaded"}
                </Badge>
              </CardHeader>
              <CardContent className="flex-1 space-y-3">
                <p className="text-sm text-muted-foreground">{skill.description}</p>
                <div className="flex items-center gap-1 text-xs">
                  <span className="text-muted-foreground">Category:</span>
                  <span className="text-primary font-medium">{skill.category}</span>
                </div>
              </CardContent>
              <CardContent className="p-3 border-t border-border/50">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => toggleSkill(skill.name)}
                  className="w-full"
                >
                  {skill.loaded ? "Unload" : "Load"}
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>
      <div className="text-xs text-muted-foreground">
        {skills.length} skills installed &bull; {skills.filter((s) => s.loaded).length} loaded
      </div>
    </div>
  );
}
