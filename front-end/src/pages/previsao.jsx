import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Upload } from "lucide-react"
import Header from "@/components/Header"

export default function PrevisaoScreen() {
  return (
      <div >
        <Header/>
        <div className="flex justify-center items-center min-h-screen">
          <Card className="w-full max-w-5xl h-[70vh] flex items-center justify-center border border-gray-400">
                <CardContent className="flex flex-col items-center justify-center text-center">
                <Upload className="w-10 h-10 mb-2" />
                <span className="text-sm text-gray-600">Solte a imagem aqui</span>
                </CardContent>
            </Card>
        </div>
      </div>
  )
}
