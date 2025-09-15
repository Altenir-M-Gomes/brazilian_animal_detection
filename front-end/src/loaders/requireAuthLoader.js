import { redirect } from "react-router-dom";

export const requireAuthLoader = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    throw redirect("/login");
  }
  return null;
};