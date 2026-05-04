import { Power, Trash2 } from "lucide-react";
import { useState } from "react";
import { api } from "../api/client.js";

const emptyCriteria = {
  category: "",
  name: "",
  weight: "",
};

export default function CriteriaPage({ criteria, onChanged, setError }) {
  const [form, setForm] = useState(emptyCriteria);
  const [saving, setSaving] = useState(false);

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      await api.createCriteria({
        ...form,
        weight: Number(form.weight || 0),
      });
      setForm(emptyCriteria);
      await onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const toggleStatus = async (item) => {
    setError("");
    try {
      await api.setCriteriaStatus(item.id, !item.is_active);
      await onChanged();
    } catch (err) {
      setError(err.message);
    }
  };

  const removeCriteria = async (id) => {
    setError("");
    try {
      await api.deleteCriteria(id);
      await onChanged();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="stack">
      <section className="panel">
        <div className="section-heading">
          <h2>Add Criterion</h2>
          <span>Weights are added into each faculty score</span>
        </div>

        <form className="inline-form" onSubmit={submit}>
          <input
            placeholder="Category"
            value={form.category}
            onChange={(event) =>
              setForm((current) => ({ ...current, category: event.target.value }))
            }
            required
          />
          <input
            placeholder="Criterion name"
            value={form.name}
            onChange={(event) =>
              setForm((current) => ({ ...current, name: event.target.value }))
            }
            required
          />
          <input
            min="0"
            placeholder="Weight"
            step="0.1"
            type="number"
            value={form.weight}
            onChange={(event) =>
              setForm((current) => ({ ...current, weight: event.target.value }))
            }
            required
          />
          <button disabled={saving} type="submit">
            {saving ? "Adding..." : "Add Criterion"}
          </button>
        </form>
      </section>

      <section className="panel">
        <div className="section-heading">
          <h2>All Criteria</h2>
          <span>{criteria.length} records</span>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Name</th>
                <th>Weight</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {criteria.map((item) => (
                <tr key={item.id}>
                  <td>{item.category}</td>
                  <td>{item.name}</td>
                  <td>{Number(item.weight).toFixed(2)}</td>
                  <td>
                    <span className={item.is_active ? "status on" : "status"}>
                      {item.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td>
                    <div className="action-row">
                      <button
                        className="icon-button"
                        onClick={() => toggleStatus(item)}
                        title={item.is_active ? "Deactivate" : "Activate"}
                        type="button"
                      >
                        <Power size={16} />
                      </button>
                      <button
                        className="icon-button danger"
                        onClick={() => removeCriteria(item.id)}
                        title="Delete criterion"
                        type="button"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {criteria.length === 0 && (
                <tr>
                  <td colSpan="5" className="empty-cell">
                    No criteria records yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
