import fs from "node:fs";
import path from "node:path";
import styles from "./page.module.css";

type Task = {
  id: string;
  title: string;
  aim: string;
  highlights: string[];
  program: string;
  code: string;
};

const baseTasks: Omit<Task, "code">[] = [
  {
    id: "task-1",
    title: "Task 1 · Largest Number Using Nested If",
    aim: "Determine the largest of three numbers with nested if statements.",
    highlights: [
      "Demonstrates conditional control flow without helper utilities.",
      "Prints the evaluated numbers and the detected maximum.",
      "Relies strictly on nested branching for the decision path.",
    ],
    program: "task1_largest.php",
  },
  {
    id: "task-2",
    title: "Task 2 · Reverse String with strrev()",
    aim: "Reverse a string using PHP's strrev() function.",
    highlights: [
      "Uses PHP's built-in string helper directly.",
      "Displays both original and reversed strings for validation.",
      "Keeps the input deterministic for the documented screenshot.",
    ],
    program: "task2_reverse.php",
  },
];

const tasks: Task[] = baseTasks.map((task) => {
  const filePath = path.join(process.cwd(), "php", task.program);
  const code = fs.readFileSync(filePath, "utf8");
  return { ...task, code };
});

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.container}>
        <section className={styles.header}>
          <h1>PHP Programming Task Report</h1>
          <p>
            Two PHP exercises were implemented, validated in the sandbox, and
            compiled into a structured PDF. Download the report to review the
            aims, constraints, procedures, program listings, captured outputs,
            and conclusions for each task.
          </p>
          <div className={styles.actions}>
            <a className={styles.primary} href="/task-report.pdf">
              Download Report
            </a>
            <a
              className={styles.secondary}
              href="/task-report.pdf"
              target="_blank"
              rel="noreferrer"
            >
              Open Report in Browser
            </a>
          </div>
        </section>
        <section className={styles.tasksSection}>
          <h2>Included Tasks</h2>
          <ul className={styles.taskList}>
            {tasks.map((task) => (
              <li key={task.id} className={styles.taskCard}>
                <h3>{task.title}</h3>
                <p className={styles.aim}>
                  <strong>Aim:</strong> {task.aim}
                </p>
                <ul className={styles.highlightList}>
                  {task.highlights.map((highlight) => (
                    <li key={highlight}>{highlight}</li>
                  ))}
                </ul>
                <details className={styles.codeBlock}>
                  <summary>Show Program</summary>
                  <pre>
                    <code>{task.code}</code>
                  </pre>
                </details>
              </li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
