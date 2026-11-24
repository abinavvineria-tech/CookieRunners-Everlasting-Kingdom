import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Settings, Palette, Shield, User, Globe, Sparkles } from "lucide-react";

export default function StudioSettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
          Studio Settings
        </h1>
        <p className="text-muted-foreground">
          Cookie Run Studio configuration and preferences
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <SettingsCard
          title="Theme"
          description="Dark fantasy, royal purple, blue, gold and White Lily accents"
          icon={Palette}
          items={[
            { label: "Active theme", value: "Cookie Run Studio" },
            { label: "Primary color", value: "Royal Blue (#4a90e2)" },
            { label: "Accent color", value: "Gold (#ffd700)" },
            { label: "Background", value: "Deep Purple (#1a0b2e)" },
          ]}
        />
        <SettingsCard
          title="Profile"
          description="Everlily Nexus agent configuration"
          icon={User}
          items={[
            { label: "Profile name", value: "everlily" },
            { label: "Captain", value: "Abinav" },
            { label: "Location", value: "Tamil Nadu, India (IST)" },
            { label: "Stadium", value: "United Stadium" },
          ]}
        />
        <SettingsCard
          title="Security"
          description="Dashboard authentication and access"
          icon={Shield}
          items={[
            { label: "Auth method", value: "Basic Auth" },
            { label: "Username", value: "abinav" },
            { label: "Session token", value: "Injected by server" },
            { label: "API keys", value: "Redacted (.env)" },
          ]}
        />
        <SettingsCard
          title="System"
          description="Hermes Agent runtime information"
          icon={Settings}
          items={[
            { label: "Hermes version", value: "v0.22.2 (2026.9.24)" },
            { label: "Platform", value: "Android Termux" },
            { label: "Python", value: "3.14.6" },
            { label: "Dashboard port", value: "9119" },
          ]}
        />
        <SettingsCard
          title="Club Identity"
          description="Cookie Runners United (CRU)"
          icon={Globe}
          items={[
            { label: "Club", value: "Cookie Runners United" },
            { label: "Motto", value: "One Run. One Dream. One United." },
            { label: "Home colours", value: "Royal Blue / Gold / White" },
            { label: "Away colours", value: "White / Black / Gold" },
          ]}
        />
        <SettingsCard
          title="About"
          description="Cookie Run Studio by Everlily Nexus"
          icon={Sparkles}
          items={[
            { label: "Version", value: "1.0.0" },
            { label: "Built by", value: "Everlily Nexus" },
            { label: "License", value: "Proprietary — CRU" },
            { label: "Support", value: "Captain Abinav" },
          ]}
        />
      </div>
    </div>
  );
}

function SettingsCard({
  title,
  description,
  icon: Icon,
  items,
}: {
  title: string;
  description: string;
  icon: any;
  items: { label: string; value: string }[];
}) {
  return (
    <Card className="flex flex-col">
      <CardHeader>
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-primary" />
          <CardTitle className="text-sm font-semibold text-foreground">{title}</CardTitle>
        </div>
        <p className="text-xs text-muted-foreground mt-1">{description}</p>
      </CardHeader>
      <CardContent className="space-y-2">
        {items.map((item, i) => (
          <div key={i} className="flex justify-between text-sm">
            <span className="text-muted-foreground">{item.label}</span>
            <span className="text-foreground font-mono">{item.value}</span>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
