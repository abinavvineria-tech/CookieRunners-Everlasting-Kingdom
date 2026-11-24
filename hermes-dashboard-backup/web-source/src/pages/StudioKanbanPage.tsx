import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Plus, CheckCircle2, RefreshCw, Trash2 } from "lucide-react";

type KanbanColumn = {
  id: string;
  title: string;
  color: string;
  tasks: KanbanTask[];
};

type KanbanTask = {
  id: string;
  title: string;
  description: string;
  status: "todo" | "in_progress" | "review" | "done";
  priority: "low" | "medium" | "high";
  createdAt: string;
};

const COLUMNS: KanbanColumn[] = [
  { id: "todo", title: "To Do", color: "#6b7280", tasks: [] },
  { id: "in_progress", title: "In Progress", color: "#4a90e2", tasks: [] },
  { id: "review", title: "Review", color: "#7c3aed", tasks: [] },
  { id: "done", title: "Done", color: "#22c55e", tasks: [] },
];

export default function StudioKanbanPage() {
  const [columns, setColumns] = useState<KanbanColumn[]>(COLUMNS);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDesc, setNewTaskDesc] = useState("");
  const [newTaskPriority, setNewTaskPriority] = useState<"low" | "medium" | "high">("medium");

  const loadTasks = () => {
    try {
      const stored = localStorage.getItem("cru-kanban-tasks");
      if (stored) {
        const parsed = JSON.parse(stored);
        setColumns(parsed);
      }
    } catch { /* ignore */ }
  };

  const saveTasks = (next: KanbanColumn[]) => {
    setColumns(next);
    try {
      localStorage.setItem("cru-kanban-tasks", JSON.stringify(next));
    } catch { /* ignore */ }
  };

  const addTask = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;
    const task: KanbanTask = {
      id: crypto.randomUUID(),
      title: newTaskTitle,
      description: newTaskDesc,
      status: "todo",
      priority: newTaskPriority,
      createdAt: new Date().toISOString(),
    };
    const next = [...columns];
    const todoIdx = next.findIndex((c) => c.id === "todo");
    next[todoIdx].tasks.push(task);
    saveTasks(next);
    setNewTaskTitle("");
    setNewTaskDesc("");
    setNewTaskPriority("medium");
  };

  const moveTask = (taskId: string, fromId: string, toId: string) => {
    const next = columns.map((c) => ({ ...c, tasks: [...c.tasks] }));
    const fromCol = next.find((c) => c.id === fromId);
    const toCol = next.find((c) => c.id === toId);
    if (!fromCol || !toCol) return;
    const taskIdx = fromCol.tasks.findIndex((t) => t.id === taskId);
    if (taskIdx < 0) return;
    const [task] = fromCol.tasks.splice(taskIdx, 1);
    task.status = toId as KanbanTask["status"];
    toCol.tasks.push(task);
    saveTasks(next);
  };

  const deleteTask = (taskId: string) => {
    setColumns(columns.map((c) => ({ ...c, tasks: c.tasks.filter((t) => t.id !== taskId) })));
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-display font-bold text-foreground tracking-tight">
            Kanban Board
          </h1>
          <p className="text-muted-foreground">
            Cookie Runners United task board &mdash; To Do, In Progress,
            Review, Done
          </p>
        </div>
        <Button onClick={loadTasks} className="flex items-center gap-2">
          <RefreshCw className="h-4 w-4" /> Reload
        </Button>
      </div>

      <form onSubmit={addTask} className="flex gap-2 max-w-md">
        <input
          className="flex-1 h-10 px-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          placeholder="New task title…"
          value={newTaskTitle}
          onChange={(e) => setNewTaskTitle(e.target.value)}
        />
        <input
          className="flex-1 h-10 px-3 rounded-lg border border-input bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          placeholder="Description…"
          value={newTaskDesc}
          onChange={(e) => setNewTaskDesc(e.target.value)}
        />
        <select
          className="h-10 px-3 rounded-lg border border-input bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
          value={newTaskPriority}
          onChange={(e) => setNewTaskPriority(e.target.value as any)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
        <Button type="submit" className="h-10 px-4">
          <Plus className="h-4 w-4" /> Add
        </Button>
      </form>

      <div className="flex gap-3 overflow-x-auto pb-4">
        {columns.map((column) => (
          <Card
            key={column.id}
            className="w-72 flex flex-col shrink-0 border-border"
            style={{ borderColor: column.color }}
          >
            <CardHeader className="flex flex-row items-center justify-between py-2">
              <CardTitle className="text-sm font-semibold text-foreground">
                {column.title}
              </CardTitle>
              <Badge variant="outline" className="text-xs border border-border/50">
                {column.tasks.length}
              </Badge>
            </CardHeader>
            <CardContent className="flex-1 p-3 space-y-3 min-h-[20rem]">
              {column.tasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  columnId={column.id}
                  onMove={moveTask}
                  onDelete={deleteTask}
                />
              ))}
              {column.tasks.length === 0 && (
                <div className="text-[10px] text-muted-foreground text-center mt-2">
                  Empty
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

function TaskCard({
  task,
  columnId,
  onMove,
  onDelete,
}: {
  task: KanbanTask;
  columnId: string;
  onMove: (taskId: string, fromId: string, toId: string) => void;
  onDelete: (taskId: string) => void;
}) {
  return (
    <div className="flex flex-col gap-2 p-3 rounded-lg border border-border/50 bg-card text-card-foreground shadow-sm cursor-grab active:cursor-grabbing">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-foreground">{task.title}</span>
        <Badge variant="outline" className="text-[10px] border border-border/50">
          {task.priority}
        </Badge>
      </div>
      {task.description && (
        <p className="text-[11px] text-muted-foreground line-clamp-2">
          {task.description}
        </p>
      )}
      <div className="flex items-center justify-between pt-2 text-[10px]">
        <span className="text-muted-foreground">{task.priority} priority</span>
        <div className="flex gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 p-1 text-muted-foreground hover:text-primary hover:bg-primary/10"
            onClick={(e) => {
              e.stopPropagation();
              onMove(task.id, columnId, nextColumn(columnId));
            }}
          >
            <CheckCircle2 className="h-4 w-4" />
          </Button>
          <Button
            variant="destructive"
            size="icon"
            className="h-6 w-6 p-1 text-muted-foreground hover:text-destructive hover:bg-destructive/10"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(task.id);
            }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}

function nextColumn(current: string): string {
  const order = ["todo", "in_progress", "review", "done"];
  const idx = order.indexOf(current);
  return order[Math.min(idx + 1, order.length - 1)];
}
