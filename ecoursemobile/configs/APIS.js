import axios from "axios";
const BASE_URL = "https://thanhduong.pythonanywhere.com/";

export const endpoints = {
  categories: "/categories/",
  courses: "/courses/",
  lessons: (courseId) => `/courses/${courseId}/lessons`,
  "lesson-details": (lessonId) => `/lessons/${lessonId}/`,
  comments: (lessonId) => `/lessons/${lessonId}/comments/`,
  login: "/o/token",
  "current-user": "/users/current-user/",
  register: "/users/",
};

export const authApi = (accessToken) =>
  axios.create({
    headers: {
      Authorization: `bearer ${accessToken}`,
    },
  });

export default axios.create({
  baseURL: BASE_URL,
});
