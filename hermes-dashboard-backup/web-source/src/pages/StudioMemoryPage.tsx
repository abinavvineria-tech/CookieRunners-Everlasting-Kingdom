import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Database, FileText, Brain, Sparkles } from "lucide-react";

export default function StudioMemoryPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Memory Centre
          </h1>
          <p className="text-muted-foreground">
            Inspect Everlily Nexus profile memory (MEMORY.md, USER.md)
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <MemoryCard
          title="MEMORY.md"
          description="Agent notes — environment, conventions, tool quirks, lessons"
          icon={Database}
          path="MEMORY.md"
        />
        <MemoryCard
          title="USER.md"
          description="User profile — who Captain Abinav is, preferences, CRU identity"
          icon={FileText}
          path="USER.md"
        />
        <MemoryCard
          title="Profile Identity"
          description="Everlily Nexus — Captain Abinav&rsquo;s personal AI agent"
          icon={Brain}
          path="profile.yaml"
        />
        <MemoryCard
          title="Session State"
          description="Active sessions, conversation history, state.db"
          icon={Sparkles}
          path="state.db"
        />
      </div>
    </div>
  );
}

function MemoryCard({
  title,
  description,
  icon: Icon,
  path,
}: {
  title: string;
  description: string;
  icon: any;
  path: string;
}) {
  return (
    <Card className="flex flex-col">
      <CardHeader className="flex flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-primary" />
          <CardTitle className="text-sm font-semibold text-foreground">{title}</CardTitle>
        </div>
      </CardHeader>
      <CardContent className="flex-1 space-y-3">
        <p className="text-sm text-muted-foreground">{description}</p>
        <div className="bg-[#0f0a1e] p-3 rounded-lg border border-border/50 overflow-x-auto">
          <pre className="text-xs font-mono text-muted-foreground whitespace-pre-wrap">
            Profile: ~/.hermes/profiles/everlily/memories/{path}
          </pre>
        </div>
        <div className="pt-2 text-xs text-muted-foreground">
          Memory files are stored under the everlily profile at
          <code className="text-primary">~/.hermes/profiles/everlily/memories/</code>.
        </div>
      </CardContent>
    </Card>
  );
}
