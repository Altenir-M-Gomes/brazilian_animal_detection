import { Card, CardContent } from "@/components/ui/card";
import { Upload, FolderOpen } from "lucide-react";
import Header from "@/components/Header";
import { useRef } from "react";

export default function PrevisaoScreen() {
  const fileInputRef = useRef(null);
  const folderInputRef = useRef(null);

  const handleCardClick = () => {
    fileInputRef.current?.click();
  };

  const handleFolderClick = () => {
    folderInputRef.current?.click();
  };

  const handleFileChange = async (event) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    console.log(`📄 Arquivo selecionado:`, files[0].name);

    const formData = new FormData();
    formData.append("file", files[0]);

    try {
      const response = await fetch( `${import.meta.env.VITE_API_URL}/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Erro: ${response.status}`);
      const data = await response.json();
      console.log("✅ Upload concluído:", data);
    } catch (err) {
      console.error("❌ Falha no upload:", err);
    }
  };

  const handleFolderChange = async (event) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    console.log(`📁 ${files.length} arquivos encontrados na pasta:`);

    const formData = new FormData();
    for (const file of files) {
      console.log("→", file.webkitRelativePath);
      formData.append("files", file);
    }

    try {
      const response = await fetch("http://localhost:3000/api/upload-folder", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error(`Erro: ${response.status}`);
      const data = await response.json();
      console.log("✅ Upload de pasta concluído:", data);
    } catch (err) {
      console.error("❌ Falha ao enviar pasta:", err);
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
          accept="image/*"
        />

        <input
          type="file"
          ref={folderInputRef}
          onChange={handleFolderChange}
          className="hidden"
          webkitdirectory="true"
          directory=""
          multiple
        />

        <Card
          onClick={handleCardClick}
          className="w-full max-w-5xl h-[70vh] flex flex-col items-center justify-center border border-gray-400 cursor-pointer hover:bg-gray-50 transition"
        >
          <CardContent className="flex flex-col items-center justify-center text-center">
            <Upload className="w-10 h-10 mb-2" />
            <span className="text-sm text-gray-600 mb-2">
              Clique ou solte uma imagem aqui
            </span>

            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                handleFolderClick();
              }}
              className="text-blue-600 text-sm flex items-center gap-1 hover:underline"
            >
              <FolderOpen className="w-4 h-4" />
              Carregar uma pasta inteira
            </button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
