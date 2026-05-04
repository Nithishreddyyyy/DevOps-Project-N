const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || "Request failed");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  listFaculty: () => request("/api/faculty"),
  createFaculty: (payload) =>
    request("/api/faculty", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  deleteFaculty: (id) =>
    request(`/api/faculty/${id}`, {
      method: "DELETE",
    }),

  listCriteria: () => request("/api/criteria"),
  createCriteria: (payload) =>
    request("/api/criteria", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  setCriteriaStatus: (id, isActive) =>
    request(`/api/criteria/${id}/status?is_active=${isActive}`, {
      method: "PATCH",
    }),
  deleteCriteria: (id) =>
    request(`/api/criteria/${id}`, {
      method: "DELETE",
    }),

  listScores: () => request("/api/scores"),
  updateScore: (facultyId, criteria) =>
    request(`/api/scores/${facultyId}`, {
      method: "PUT",
      body: JSON.stringify({ criteria }),
    }),
};

export function pdfUrl(path) {
  return `${API_BASE}${path}`;
}
