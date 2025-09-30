import { Card, CardContent } from "@/components/ui/card";
import { Upload } from "lucide-react";
import Header from "@/components/Header";
import { useRef } from "react";

export default function PrevisaoScreen() {
  const fileInputRef = useRef(null);

  const handleCardClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event) => {
    const files = event.target.files;
    if (files && files.length > 0) {
      console.log("Arquivo selecionado:", files[0]);
    }
  };

  return (
    <div>
      <Header />
      <div className="flex justify-center items-center min-h-screen">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
        />
        <Card
          onClick={handleCardClick}
          className="w-full max-w-5xl h-[70vh] flex items-center justify-center border border-gray-400 cursor-pointer hover:bg-gray-50 transition"
        >
          <CardContent className="flex flex-col items-center justify-center text-center">
            <Upload className="w-10 h-10 mb-2" />
            <span className="text-sm text-gray-600">
              Clique ou solte a imagem aqui
            </span>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
