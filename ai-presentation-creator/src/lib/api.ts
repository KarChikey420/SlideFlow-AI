const API_BASE_URL = "http://127.0.0.1:8000";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

interface SignupResponse {
  message: string;
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Login failed");
  }

  return response.json();
}

export async function signup(name: string, email: string, password: string): Promise<SignupResponse> {
  const response = await fetch(`${API_BASE_URL}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Signup failed");
  }

  return response.json();
}

export async function generatePPT(
  topic: string,
  slideCount: number,
  token: string
): Promise<Blob> {
  const response = await fetch(`${API_BASE_URL}/generate_ppx`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ topic, slide: slideCount }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to generate presentation");
  }

  return response.blob();
}
