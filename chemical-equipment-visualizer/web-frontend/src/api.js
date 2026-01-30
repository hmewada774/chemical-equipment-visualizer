import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const login = (username, password) => {
    return api.post("/login/", { username, password });
};

export const register = (username, email, password) => {
    return api.post("/register/", { username, email, password });
};

export const getSummary = () => {
    return api.get("/summary/");
};

export const getHistory = () => {
    return api.get("/history/");
};

export const uploadFile = (formData) => {
    return api.post("/upload/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
};

export const downloadReport = async () => {
    try {
        const response = await api.get("/report/", {
            responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'report.pdf');
        document.body.appendChild(link);
        link.click();
        link.remove();
    } catch (err) {
        console.error("Report download failed", err);
    }
};

export default api;
