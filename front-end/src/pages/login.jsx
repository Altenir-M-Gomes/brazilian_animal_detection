import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useEffect } from "react";

export default function LoginPage() {
  const { register, handleSubmit, formState: { errors } } = useForm();
 
  useEffect(() => {
    Object.values(errors).forEach((error) => {
      toast.error(error.message);
    });
  }, [errors]);

  const onSubmit = async (data) => {
    
    try {
      
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Credenciais inválidas!");
      }

      const result = await response.json();
      localStorage.setItem("token", result.token);
      toast.success("Login realizado com sucesso!");
      window.location.href = "/previsao"; 
    } catch (err) {
      
      toast.error(err.message || "Erro ao fazer login");
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
                  {errors.email && (
                    <span className="text-red-500 text-sm">{errors.email.message}</span>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Senha</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="Digite sua senha aqui"
                    {...register("senha", { required: "Senha é obrigatória" })}
                    className="h-[40px] border border-gray-400 focus:border-gray-500"
                  />
                  {errors.senha && (
                    <span className="text-red-500 text-sm">{errors.senha.message}</span>
                  )}
                </div>

                <Button type="submit" className="w-full bg-[#1e3a56] h-[35px] text-white">
                  Login
                </Button>
              </form>

              <p className="text-sm pt-4">
                Não tem uma conta? <a href="/cadastrar" className="text-blue-600 hover:underline">Cadastre-se</a>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
