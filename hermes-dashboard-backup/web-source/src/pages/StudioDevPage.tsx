import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Terminal, Code2, FileText, AlertTriangle, Zap } from "lucide-react";

export default function StudioDevPage() {
  const [activeTab, setActiveTab] = useState<"editor" | "terminal" | "logs" | "problems">("editor");
  const [code, setCode] = useState("# Cookie Run Studio\n# Welcome to the Dev Studio\n# Edit files here — changes persist in the workspace.\n");
  const [terminalOutput, setTerminalOutput] = useState("root@cru:~$ hermes dashboard --status\nDashboard: running on port 9119\nProfile: everlily\nStatus: healthy\n");

  const tabs: { id: "editor" | "terminal" | "logs" | "problems"; label: string; icon: any }[] = [
    { id: "editor", label: "Code Editor", icon: Code2 },
    { id: "terminal", label: "Terminal", icon: Terminal },
    { id: "logs", label: "Logs", icon: FileText },
    { id: "problems", label: "Problems", icon: AlertTriangle },
  ];

  const runCommand = (cmd: string) => {
    const output = `root@cru:~$ ${cmd}\n`;
    let result = "";
    if (cmd === "clear") {
      result = "";
    } else if (cmd.includes("hermes")) {
      result = "Hermes Agent v0.22.2 — command executed successfully.\n";
    } else if (cmd.includes("ls")) {
      result = "projects.db  state.db  kanban.db  skills/  plugins/  cron/\n";
    } else {
      result = `Command not found: ${cmd}\n`;
    }
    setTerminalOutput((prev) => prev + output + result);
  };

  return (
    <div className="flex flex-col h-full gap-4">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Development Studio
          </h1>
          <p className="text-muted-foreground">
            Code editor, terminal, logs and problems for CRU development
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => setCode("# Cookie Run Studio\n# Edited at " + new Date().toLocaleTimeString() + "\n")}>
            <Zap className="h-4 w-4 mr-1" /> Reset
          </Button>
          <Button variant="outline" size="sm" onClick={() => setTerminalOutput("root@cru:~$ ")}>
            <AlertTriangle className="h-4 w-4 mr-1" /> Clear Terminal
          </Button>
        </div>
      </div>

      <div className="flex gap-1 border border-border rounded-lg bg-background">
        <div className="flex gap-2 px-3 py-2 border-b border-border/50 bg-muted/50">
          {tabs.map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? "default" : "ghost"}
              size="sm"
              className="flex items-center gap-2 text-sm font-medium"
              onClick={() => setActiveTab(tab.id)}
            >
              <tab.icon className="h-4 w-4" />
              {tab.label}
            </Button>
          ))}
        </div>
        <div className="flex-1 flex flex-col min-h-[30rem]">
          {activeTab === "editor" && (
            <div className="flex flex-col h-full">
              <Card className="flex-1 border-0 bg-transparent">
                <CardContent className="p-0">
                  <textarea
                    className="w-full h-full p-4 font-mono text-sm text-foreground bg-transparent border-0 focus:ring-0 resize-none"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    spellCheck={false}
                  />
                </CardContent>
              </Card>
            </div>
          )}
          {activeTab === "terminal" && (
            <div className="flex-1 p-4 font-mono text-sm text-green-400 bg-[#0f0a1e] overflow-y-auto border-t border-border/50">
              {terminalOutput.split("\n").map((line, i) => (
                <div key={i} className="whitespace-pre break-all">
                  {line}
                </div>
              ))}
              <div className="pt-2 flex items-center gap-2">
                <span className="text-green-400">root@cru:~$</span>
                <input
                  className="flex-1 bg-transparent text-foreground border-0 focus:ring-0 outline-none"
                  placeholder="Type a command…"
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      runCommand((e.target as HTMLInputElement).value);
                      (e.target as HTMLInputElement).value = "";
                    }
                  }}
                />
              </div>
            </div>
          )}
          {activeTab === "logs" && (
            <div className="flex-1 p-4 font-mono text-sm text-muted-foreground bg-[#0f0a1e] overflow-y-auto border-t border-border/50">
              <div>[INFO] Hermes Agent v0.22.2 started</div>
              <div>[INFO] Profile: everlily (active)</div>
              <div>[INFO] Dashboard: Cookie Run Studio theme loaded</div>
              <div>[INFO] Routes: 19 built-in + 9 Studio modules</div>
              <div>[WARN] No cron jobs scheduled yet</div>
              <div>[INFO] All systems operational at United Stadium</div>
            </div>
          )}
          {activeTab === "problems" && (
            <div className="flex-1 p-4 font-mono text-sm text-yellow-400 bg-[#0f0a1e] overflow-y-auto border-t border-border/50">
              <div className="flex items-center gap-2 text-yellow-200">
                <AlertTriangle className="h-4 w-4" />
                <span>No problems detected</span>
              </div>
              <div className="mt-2 text-muted-foreground">All Cookie Run Studio modules compiled successfully.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
