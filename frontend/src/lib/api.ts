import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      if (typeof window !== "undefined") {
        localStorage.removeItem("token");
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (data: { username: string; password: string }) =>
    api.post("/v1/auth/login/", data),
  register: (data: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
  }) => api.post("/v1/auth/register/", data),
  logout: () => api.post("/v1/auth/logout/"),
  getProfile: () => api.get("/v1/auth/profile/"),
  updateProfile: (data: Record<string, unknown>) =>
    api.put("/v1/auth/profile/", data),
};

// Meetings API
export const meetingsAPI = {
  list: (params?: Record<string, string>) =>
    api.get("/v1/meetings/", { params }),
  get: (id: number) => api.get(`/v1/meetings/${id}/`),
  create: (data: FormData) =>
    api.post("/v1/meetings/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    }),
  update: (id: number, data: Record<string, unknown>) =>
    api.patch(`/v1/meetings/${id}/`, data),
  delete: (id: number) => api.delete(`/v1/meetings/${id}/`),
  process: (id: number) => api.post(`/v1/meetings/${id}/process/`),
  getStatus: (id: number) => api.get(`/v1/meetings/${id}/status/`),
  addParticipants: (id: number, participants: Record<string, unknown>[]) =>
    api.post(`/v1/meetings/${id}/add_participants/`, participants),
};

// Tasks API
export const tasksAPI = {
  list: (params?: Record<string, string>) =>
    api.get("/v1/tasks/", { params }),
  get: (id: number) => api.get(`/v1/tasks/${id}/`),
  updateStatus: (id: number, status: string) =>
    api.patch(`/v1/tasks/${id}/update_status/`, { status }),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () => api.get("/v1/analytics/dashboard/"),
  getTrends: (days?: number) =>
    api.get("/v1/analytics/trends/", { params: { days } }),
};

// AI API
export const aiAPI = {
  askQuestion: (meetingId: number, question: string) =>
    api.post("/v1/ai/qa/", { meeting_id: meetingId, question }),
  searchMeetings: (query: string) =>
    api.post("/v1/ai/search/", { query }),
};

// Notifications API
export const notificationsAPI = {
  list: () => api.get("/v1/notifications/"),
  getUnreadCount: () => api.get("/v1/notifications/unread_count/"),
  markRead: (id: number) => api.patch(`/v1/notifications/${id}/mark_read/`),
};
