const API_BASE = 'http://localhost:8000';

export async function login(username, password) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Error de autenticación');
  }
  return res.json();
}

export async function getKpis() {
  const res = await fetch(`${API_BASE}/api/stats/kpis`);
  return res.json();
}

export async function getDrilldownPeriodos() {
  const res = await fetch(`${API_BASE}/api/stats/drilldown/periodos`);
  return res.json();
}

export async function getDrilldownHabitats(periodoId) {
  const res = await fetch(`${API_BASE}/api/stats/drilldown/habitats/${periodoId}`);
  return res.json();
}

export async function getDrilldownDinos(periodoId, habitatId) {
  const res = await fetch(`${API_BASE}/api/stats/drilldown/dinosaurios/${periodoId}/${habitatId}`);
  return res.json();
}

export async function getDinoDetail(dinoId) {
  const res = await fetch(`${API_BASE}/api/stats/dinosaurio/${dinoId}`);
  return res.json();
}
