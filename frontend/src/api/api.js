import axios from "axios";


const API_BASE_URL =
  process.env.REACT_APP_API_URL || "http://localhost:8000";
const API = axios.create({
  baseURL: API_BASE_URL
});


export const sendChatMessage = async (message, context = null) => {
  const response = await axios.post(`${API_BASE_URL}/ai/chat`, {
    message,
    context,
  });
  return response.data;
};

export const getChatHistory = async () => {
  const response = await axios.get(`${API_BASE_URL}/ai/history`);
  return response.data;
};


export const getTeamMembers = () => API.get("/team/");
export const addTeamMember = (data) =>
  API.post("/team/", data);
export const deleteTeamMember = (id) =>
  API.delete(`/team/${id}`);

export const getProjects = () => API.get("/projects/");
export const addProject = (data) =>
  API.post("/projects/", data);
export const deleteProject = (id) =>
  API.delete(`/projects/${id}`);

export const getUpdates = () => API.get("/updates/");
export const addUpdate = (data) =>
  API.post("/updates/", data);
export const deleteUpdate = (id) =>
  API.delete(`/updates/${id}`);
