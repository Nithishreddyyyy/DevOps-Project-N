import { Download, Minus, Plus, Save } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { api, pdfUrl } from "../api/client.js";

export default function ScoresPage({ scores, criteria, onChanged, setError }) {
  const activeCriteria = useMemo(
    () => criteria.filter((item) => item.is_active),
    [criteria],
  );

  return (
    <div className="stack">
      <section className="panel">
        <div className="section-heading">
          <h2>Faculty Appraisal Scores</h2>
          <a className="link-button" href={pdfUrl("/scores/pdf/all")}>
            <Download size={16} />
            <span>All Reports</span>
          </a>
        </div>

        <div className="score-list">
          {scores.map((faculty) => (
            <ScoreEditor
              activeCriteria={activeCriteria}
              faculty={faculty}
              key={faculty.id}
              onChanged={onChanged}
              setError={setError}
            />
          ))}
          {scores.length === 0 && (
            <div className="empty-state">Add faculty to begin scoring.</div>
          )}
        </div>
      </section>
    </div>
  );
}

function ScoreEditor({ faculty, activeCriteria, onChanged, setError }) {
  const [selected, setSelected] = useState(faculty.selected_criteria || []);
  const [criterionName, setCriterionName] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setSelected(faculty.selected_criteria || []);
  }, [faculty.selected_criteria]);

  const grouped = useMemo(() => {
    return selected.reduce((map, name) => {
      map.set(name, (map.get(name) || 0) + 1);
      return map;
    }, new Map());
  }, [selected]);

  const addCriterion = () => {
    if (!criterionName) {
      return;
    }
    setSelected((current) => [...current, criterionName]);
    setCriterionName("");
  };

  const removeCriterion = (name) => {
    setSelected((current) => {
      const index = current.indexOf(name);
      if (index === -1) {
        return current;
      }
      return [...current.slice(0, index), ...current.slice(index + 1)];
    });
  };

  const save = async () => {
    setSaving(true);
    setError("");

    try {
      await api.updateScore(faculty.id, selected);
      await onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <article className="score-card">
      <div className="score-card-header">
        <div>
          <h3>{faculty.name}</h3>
          <span>{faculty.department}</span>
        </div>
        <strong>{Number(faculty.total_score || 0).toFixed(2)}</strong>
      </div>

      <div className="chip-list">
        {[...grouped.entries()].map(([name, count]) => (
          <span className="chip" key={name}>
            {name}
            <b>{count}</b>
            <button
              onClick={() => removeCriterion(name)}
              title={`Remove ${name}`}
              type="button"
            >
              <Minus size={13} />
            </button>
          </span>
        ))}
        {selected.length === 0 && <span className="muted">No criteria selected</span>}
      </div>

      <div className="score-actions">
        <select
          value={criterionName}
          onChange={(event) => setCriterionName(event.target.value)}
        >
          <option value="">Add criterion...</option>
          {activeCriteria.map((item) => (
            <option key={item.id} value={item.name}>
              {item.name}
            </option>
          ))}
        </select>
        <button className="icon-button" onClick={addCriterion} type="button">
          <Plus size={16} />
        </button>
        <button className="icon-text-button" disabled={saving} onClick={save} type="button">
          <Save size={16} />
          <span>{saving ? "Saving" : "Save"}</span>
        </button>
        <a className="icon-text-button" href={pdfUrl(`/scores/pdf/${faculty.id}`)}>
          <Download size={16} />
          <span>PDF</span>
        </a>
      </div>
    </article>
  );
}
