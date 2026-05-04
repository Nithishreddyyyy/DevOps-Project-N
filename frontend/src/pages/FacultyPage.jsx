import { Trash2 } from "lucide-react";
import { useState } from "react";
import { api } from "../api/client.js";

const emptyFaculty = {
  name: "",
  department: "",
  designation: "",
  contact: "",
  qualifications: "",
  experience: "",
  doj: "",
  categories: [],
};

export default function FacultyPage({ faculty, onChanged, setError }) {
  const [form, setForm] = useState(emptyFaculty);
  const [saving, setSaving] = useState(false);

  const updateField = (field, value) => {
    if (field === "contact") {
      value = value.replace(/\D/g, "").slice(0, 10);
    }
    setForm((current) => ({ ...current, [field]: value }));
  };

  const submit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError("");

    try {
      await api.createFaculty({
        ...form,
        experience: Number(form.experience || 0),
      });
      setForm(emptyFaculty);
      await onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const removeFaculty = async (id) => {
    setError("");
    try {
      await api.deleteFaculty(id);
      await onChanged();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="stack">
      <section className="panel">
        <div className="section-heading">
          <h2>Add Faculty</h2>
          <span>Faculty profile and appointment details</span>
        </div>

        <form className="form-grid" onSubmit={submit}>
          <Field
            label="Name"
            value={form.name}
            onChange={(value) => updateField("name", value)}
            required
          />
          <Field
            label="Department"
            value={form.department}
            onChange={(value) => updateField("department", value)}
            required
          />
          <Field
            label="Designation"
            value={form.designation}
            onChange={(value) => updateField("designation", value)}
            required
          />
          <Field
            label="Contact"
            value={form.contact}
            onChange={(value) => updateField("contact", value)}
            inputMode="numeric"
          />
          <Field
            label="Qualifications"
            value={form.qualifications}
            onChange={(value) => updateField("qualifications", value)}
          />
          <Field
            label="Experience"
            type="number"
            min="0"
            value={form.experience}
            onChange={(value) => updateField("experience", value)}
          />
          <Field
            label="Date of Joining"
            type="date"
            value={form.doj}
            onChange={(value) => updateField("doj", value)}
            required
          />
          <div className="form-actions">
            <button disabled={saving} type="submit">
              {saving ? "Saving..." : "Save Faculty"}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="section-heading">
          <h2>All Faculty</h2>
          <span>{faculty.length} records</span>
        </div>

        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Department</th>
                <th>Designation</th>
                <th>DOJ</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {faculty.map((item) => (
                <tr key={item.id}>
                  <td>{item.name}</td>
                  <td>{item.department}</td>
                  <td>{item.designation}</td>
                  <td>{item.doj}</td>
                  <td>
                    <button
                      className="icon-button danger"
                      onClick={() => removeFaculty(item.id)}
                      title="Delete faculty"
                      type="button"
                    >
                      <Trash2 size={16} />
                    </button>
                  </td>
                </tr>
              ))}
              {faculty.length === 0 && (
                <tr>
                  <td colSpan="5" className="empty-cell">
                    No faculty records yet.
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

function Field({ label, value, onChange, type = "text", ...props }) {
  return (
    <label className="field">
      <span>{label}</span>
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        {...props}
      />
    </label>
  );
}
