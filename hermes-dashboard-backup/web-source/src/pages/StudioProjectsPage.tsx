import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, Folder, Database, Edit3, Trash2 } from "lucide-react";

type Project = {
  id: string;
  name: string;
  description: string;
  status: "active" | "planning" | "completed" | "archived";
  createdAt: string;
};

export default function StudioProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: "1",
      name: "Cookie Run Studio",
      description: "Hermes dashboard upgrade for Cookie Runners United",
      status: "active",
      createdAt: new Date().toISOString(),
    },
    {
      id: "2",
      name: "CRU Squad Management",
      description: "Cookie Runners United player and match tracking",
      status: "planning",
      createdAt: new Date().toISOString(),
    },
  ]);
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");

  const addProject = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    const project: Project = {
      id: crypto.randomUUID(),
      name: newName,
      description: newDesc,
      status: "planning",
      createdAt: new Date().toISOString(),
    };
    setProjects([...projects, project]);
    setNewName("");
    setNewDesc("");
  };

  const deleteProject = (id: string) => {
    setProjects(projects.filter((p) => p.id !== id));
  };

  const statusBadge = (status: string) => {
    const variants: Record<string, string> = {
      active: "bg-green/10 text-green border-green/20",
      planning: "bg-yellow/10 text-yellow border-yellow/20",
      completed: "bg-blue/10 text-blue border-blue/20",
      archived: "bg-gray/10 text-gray border-gray/20",
    };
    return variants[status] || variants.active;
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Project Manager
          </h1>
          <p className="text-muted-foreground">
            Create and organize Cookie Runners United projects
          </p>
        </div>
        <Button onClick={() => {}} className="flex items-center gap-2">
          <Database className="h-4 w-4" /> Refresh
        </Button>
      </div>

      <form onSubmit={addProject} className="flex flex-col md:flex-row gap-3 max-w-md">
        <input
          className="flex-1 h-10 px-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          placeholder="Project name…"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <input
          className="flex-1 h-10 px-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          placeholder="Description…"
          value={newDesc}
          onChange={(e) => setNewDesc(e.target.value)}
        />
        <Button type="submit" className="h-10 px-4">
          <Plus className="h-4 w-4" /> Create
        </Button>
      </form>

      <div className="grid gap-4 md:grid-cols-3">
        {projects.map((project) => (
          <Card key={project.id} className="flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="font-semibold text-foreground">{project.name}</CardTitle>
              <Badge variant="outline" className={statusBadge(project.status)}>
                {project.status}
              </Badge>
            </CardHeader>
            <CardContent className="flex-1 space-y-3">
              <p className="text-sm text-muted-foreground line-clamp-2">
                {project.description}
              </p>
              <div className="text-xs text-muted-foreground">
                Created {new Date(project.createdAt).toLocaleDateString()}
              </div>
            </CardContent>
            <div className="flex gap-2 p-3 border-t border-border/50">
              <Button
                variant="ghost"
                size="sm"
                className="flex-1"
                onClick={() => {}}
              >
                <Edit3 className="h-4 w-4 mr-1" /> Edit
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => deleteProject(project.id)}
              >
                <Trash2 className="h-4 w-4 mr-1" /> Delete
              </Button>
            </div>
          </Card>
        ))}
        {projects.length === 0 && (
          <Card className="col-span-3 flex flex-col items-center justify-center py-12">
            <Folder className="h-12 w-12 text-muted-foreground mb-3" />
            <p className="text-muted-foreground">No projects yet. Create your first one above.</p>
          </Card>
        )}
      </div>
    </div>
  );
}
