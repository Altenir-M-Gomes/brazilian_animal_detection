import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function CadastrarPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  // Mostrar erros com toast
  useEffect(() => {
    Object.values(errors).forEach((error) => {
      toast.error(error.message);
    });
  }, [errors]);

  const onSubmit = async (data) => {
    data = { 'nome': 'aaa', 'sobrenome': 'aaa', ...data }
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/users/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const resData = await response.json();
        throw new Error(resData.message || "Erro ao criar conta");
      }

      toast.success("Conta criada com sucesso!");
      window.location.href = "/login"; 
    } catch (err) {
      toast.error(err.message || "Erro ao criar conta");
    }
  };

  return (
    <div className="flex h-screen w-screen">
      <ToastContainer position="top-right" autoClose={3000} theme="light" />
      <div className="w-1/2 bg-[#1e3a56]"></div>
      <div className="w-1/2 flex items-center justify-center">
        <div>
          <Card className="shadow-lg rounded-2xl w-96 py-4 border border-gray-400">
            <CardContent className="p-4 space-y-4">
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="Digite seu email aqui"
                    {...register("email", { required: "E-mail é obrigatório" })}
                    className="h-[40px] border border-gray-400 focus:border-gray-500"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="senha">Senha</Label>
                  <Input
                    id="senha"
                    type="password"
                    placeholder="Digite sua senha aqui"
                    {...register("senha", { required: "Senha é obrigatória" })}
                    className="h-[40px] border border-gray-400 focus:border-gray-500"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmSenha">Confirme a senha</Label>
                  <Input
                    id="confirmSenha"
                    type="password"
                    placeholder="Confirme sua senha"
                    {...register("confirmSenha", { required: "Confirmação é obrigatória" })}
                    className="h-[40px] border border-gray-400 focus:border-gray-500"
                  />
                </div>

                <Button type="submit" className="w-full bg-[#1e3a56] h-[35px] text-white">
                  Criar conta
                </Button>
              </form>

              <p className="text-sm pt-4">
                Já possui uma conta?{" "}
                <a href="/login" className="text-blue-600 hover:underline">
                  Fazer login
                </a>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
