import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  return (
    <div className="flex h-screen w-screen">
      <div className="w-1/2 bg-[#1e3a56]"></div>
      <div className="w-1/2 flex items-center justify-center">
        <div>
        <Card className="shadow-lg rounded-2xl w-96 py-4 border border-gray-400">
            <CardContent className="p-4 space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input className="h-[40px] border border-gray-400 focus:border-gray-500" id="email" type="email" placeholder="Digite seu email aqui" />
              </div>
              <div className="space-y-2">
                <Label  htmlFor="password">Senha</Label>
                <Input className="h-[40px] border border-gray-400 focus:border-gray-500" id="password" type="password" placeholder="Digite sua senha aqui" />
              </div>
                <Button href="/login" className="w-full bg-[#1e3a56] h-[35px] text-white">
                    Login
                </Button>
              <p className="text-sm pt-4">
                Não tem uma conta? <a href="#" className="text-blue-600 hover:underline">Cadastre-se</a>
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
