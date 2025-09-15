import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  createBrowserRouter,
  Outlet,
  RouterProvider,
} from "react-router-dom";
import "./index.css";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/login";
import PrevisaoScreen from "./pages/previsao";
import { ToastContainer } from "react-toastify";
import CadastrarPage from "./pages/cadastrar";
import { requireAuthLoader } from "./loaders/requireAuthLoader";

const router = createBrowserRouter([
  {
    element: (
      <AuthProvider>
        <Outlet />
      </AuthProvider>
    ),
    children: [
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/previsao",
        element: <PrevisaoScreen />,
        loader: requireAuthLoader

      },
       {
        path: "/cadastrar",
        element: <CadastrarPage />,
      },
    
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ToastContainer
      position="top-right"
      autoClose={3000}
      hideProgressBar={false}
      newestOnTop
      closeOnClick
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="light"
    />
    <RouterProvider router={router} />
  </StrictMode>
);