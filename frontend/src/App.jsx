import { useEffect, useMemo, useState } from "react";
import {
  Award,
  BarChart3,
  GraduationCap,
  LayoutDashboard,
  ListChecks,
} from "lucide-react";
import { api } from "./api/client.js";
import FacultyPage from "./pages/FacultyPage.jsx";
import CriteriaPage from "./pages/CriteriaPage.jsx";
import ScoresPage from "./pages/ScoresPage.jsx";

const navItems = [
  { id: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { id: "faculty", label: "Faculty", icon: GraduationCap },
  { id: "criteria", label: "Criteria", icon: ListChecks },
  { id: "scores", label: "Scores", icon: Award },
];

export default function App() {
  const [activePage, setActivePage] = useState("dashboard");
  const [faculty, setFaculty] = useState([]);
  const [criteria, setCriteria] = useState([]);
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refreshAll = async () => {
    setError("");
    const [facultyData, criteriaData, scoreData] = await Promise.all([
      api.listFaculty(),
      api.listCriteria(),
      api.listScores(),
    ]);
    setFaculty(facultyData);
    setCriteria(criteriaData);
    setScores(scoreData.scores);
  };

  useEffect(() => {
    refreshAll()
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const metrics = useMemo(() => {
    const activeCriteria = criteria.filter((item) => item.is_active).length;
    const averageScore =
      scores.length === 0
        ? 0
        : scores.reduce((sum, item) => sum + Number(item.total_score || 0), 0) /
          scores.length;

    return {
      facultyCount: faculty.length,
      criteriaCount: criteria.length,
      activeCriteria,
      averageScore,
    };
  }, [criteria, faculty, scores]);

  const pageTitle =
    navItems.find((item) => item.id === activePage)?.label || "Dashboard";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <BarChart3 size={22} />
          </div>
          <div>
            <strong>Faculty Appraisal</strong>
            <span>Increment Management</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="Main navigation">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={activePage === item.id ? "active" : ""}
                onClick={() => setActivePage(item.id)}
                type="button"
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Ramaiah Institute of Technology</span>
            <h1>{pageTitle}</h1>
          </div>
          <button className="ghost-button" onClick={refreshAll} type="button">
            Refresh
          </button>
        </header>

        {error && <div className="alert">{error}</div>}

        {loading ? (
          <div className="panel">Loading faculty appraisal data...</div>
        ) : (
          <>
            {activePage === "dashboard" && (
              <Dashboard metrics={metrics} scores={scores} />
            )}
            {activePage === "faculty" && (
              <FacultyPage
                faculty={faculty}
                onChanged={refreshAll}
                setError={setError}
              />
            )}
            {activePage === "criteria" && (
              <CriteriaPage
                criteria={criteria}
                onChanged={refreshAll}
                setError={setError}
              />
            )}
            {activePage === "scores" && (
              <ScoresPage
                scores={scores}
                criteria={criteria}
                onChanged={refreshAll}
                setError={setError}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

function Dashboard({ metrics, scores }) {
  const topScores = [...scores]
    .sort((a, b) => Number(b.total_score || 0) - Number(a.total_score || 0))
    .slice(0, 5);

  return (
    <div className="stack">
      <section className="metric-grid">
        <Metric label="Faculty" value={metrics.facultyCount} />
        <Metric label="Criteria" value={metrics.criteriaCount} />
        <Metric label="Active Criteria" value={metrics.activeCriteria} />
        <Metric label="Average Score" value={metrics.averageScore.toFixed(2)} />
      </section>

      <section className="panel">
        <div className="section-heading">
          <h2>Score Overview</h2>
          <span>{topScores.length} faculty shown</span>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Department</th>
                <th>Criteria Count</th>
                <th>Total Score</th>
              </tr>
            </thead>
            <tbody>
              {topScores.map((faculty) => (
                <tr key={faculty.id}>
                  <td>{faculty.name}</td>
                  <td>{faculty.department}</td>
                  <td>{faculty.selected_criteria.length}</td>
                  <td>{Number(faculty.total_score || 0).toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function Metric({ label, value }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
