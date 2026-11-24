import { useState, useEffect } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Pause, RefreshCw } from "lucide-react";
import { api } from "@/lib/api";

type CronJob = {
  id: string;
  name: string;
  schedule: string;
  command: string;
  enabled: boolean;
  lastRun: string | null;
  nextRun: string | null;
};

export default function StudioJobsPage() {
  const [jobs, setJobs] = useState<CronJob[]>([
    {
      id: "1",
      name: "CRU Daily Report",
      schedule: "0 8 * * *",
      command: "hermes cru report --daily",
      enabled: true,
      lastRun: null,
      nextRun: "Tomorrow 08:00 IST",
    },
    {
      id: "2",
      name: "Matchday Reminder",
      schedule: "0 18 * * *",
      command: "hermes matchday notify",
      enabled: true,
      lastRun: null,
      nextRun: "Today 18:00 IST",
    },
  ]);

  useEffect(() => {
    api.getCronJobs?.()
      .then((resp) => {
        const fetched = (resp as any)?.jobs;
        if (Array.isArray(fetched)) {
          setJobs(fetched.map((j: any) => ({
            id: j.id,
            name: j.name,
            schedule: j.schedule,
            command: j.command,
            enabled: j.enabled ?? true,
            lastRun: j.last_run ?? null,
            nextRun: j.next_run ?? null,
          })));
        }
      })
      .catch(() => { /* keep defaults */ });
  }, []);

  const toggleJob = (id: string) => {
    setJobs(jobs.map((j) =>
      j.id === id ? { ...j, enabled: !j.enabled } : j
    ));
  };

  const statusColor = (enabled: boolean) => enabled ? "text-green" : "text-muted-foreground";

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Job Centre
          </h1>
          <p className="text-muted-foreground">
            Monitor cron jobs and schedules for Cookie Runners United
          </p>
        </div>
        <Button onClick={() => {}} className="flex items-center gap-2">
          <RefreshCw className="h-4 w-4" /> Refresh
        </Button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-border/50">
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Name</th>
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Schedule</th>
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Command</th>
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Next Run</th>
              <th className="pb-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id} className="border-b border-border/50 hover:bg-accent/50 transition-colors">
                <td className="py-3 text-sm font-medium text-foreground">{job.name}</td>
                <td className="py-3 text-sm text-muted-foreground font-mono">{job.schedule}</td>
                <td className="py-3 text-sm text-muted-foreground font-mono">{job.command}</td>
                <td className="py-3">
                  <Badge variant={job.enabled ? "default" : "secondary"} className="flex items-center gap-1">
                    <span className={`h-2 w-2 rounded-full ${statusColor(job.enabled)}`} />
                    {job.enabled ? "Enabled" : "Disabled"}
                  </Badge>
                </td>
                <td className="py-3 text-sm text-muted-foreground">{job.nextRun}</td>
                <td className="py-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => toggleJob(job.id)}
                  >
                    {job.enabled ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                  </Button>
                </td>
              </tr>
            ))}
            {jobs.length === 0 && (
              <tr>
                <td colSpan={6} className="py-8 text-center text-muted-foreground">
                  No cron jobs scheduled yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="text-xs text-muted-foreground">
        {jobs.length} scheduled job(s) &bull; {jobs.filter((j) => j.enabled).length} enabled
      </div>
    </div>
  );
}
