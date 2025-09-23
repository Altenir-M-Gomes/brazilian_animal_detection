import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { Card, CardContent } from "@/components/ui/card";

export default function VerificarConta() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState("Verificando sua conta...");

  useEffect(() => {
    const verificarConta = async () => {
      if (!token) {
        toast.error("Token inválido ou ausente.");
        setStatus("Erro: Token inválido.");
        return;
      }

      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/auth/verify?token=${token}`,
          { method: "GET" }
        );

        if (!response.ok) {
          throw new Error("Falha na verificação da conta.");
        }

        toast.success("Conta verificada com sucesso!");
        setStatus("Obrigado por verificar sua conta!");
      } catch (err) {
        toast.error(err.message || "Erro ao verificar conta.");
        setStatus("Erro ao verificar conta.");
      }
    };

    verificarConta();
  }, [token]);

  return (
    <div className="flex h-screen w-screen">
      <ToastContainer position="top-right" autoClose={3000} theme="light" />
      <div className="w-1/2 bg-[#1e3a56]"></div>
      <div className="w-1/2 flex items-center justify-center">
        <Card className="rounded-2xl w-96 py-6 border border-gray-400">
          <CardContent className="p-6 text-center space-y-3">
            <h1 className="text-xl font-bold text-[#1e3a56]">{status}</h1>
            <p className="text-sm text-gray-600">
              Agora você já pode fazer login e acessar sua conta.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
