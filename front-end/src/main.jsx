import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  createBrowserRouter,
  Outlet,
  RouterProvider,
  Navigate,
} from "react-router-dom";
import "./index.css";
import { AuthProvider } from "./context/AuthContext";
import Login from "./pages/login";
import PrevisaoScreen from "./pages/previsao";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import CadastrarPage from "./pages/cadastrar";
import { requireAuthLoader } from "./loaders/requireAuthLoader";
import VerificarConta from "./pages/verificarConta";

function NotFound() {
  return <h1>404 - Página não encontrada</h1>;
}

// detecta se é mobile
const isMobile = window.innerWidth < 768;

const router = createBrowserRouter([
  {
    element: (
      <AuthProvider>
        <Outlet />
      </AuthProvider>
    ),
    errorElement: <NotFound />,
    children: [
      {
        path: "/",
        element: <Navigate to="/login" replace />,
      },
      {
        path: "/login",
        element: <Login />,
      },
      {
        path: "/previsao",
        element: <PrevisaoScreen />,
        loader: requireAuthLoader,
      },
      {
        path: "/cadastrar",
        element: <CadastrarPage />,
      },
      {
        path: "/verificar-conta",
        element: <VerificarConta />,
      },
      {
        path: "*",
        element: <NotFound />,
      },
    ],
  },
]);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ToastContainer
      position={isMobile ? "bottom-center" : "top-right"} // 📱 embaixo no mobile
      autoClose={3000}
      hideProgressBar={false}
      newestOnTop
      closeOnClick
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="light"
      style={!isMobile ? { marginTop: "60px" } : undefined} // 💻 afasta do header
    />
    <RouterProvider router={router} />
  </StrictMode>
);
