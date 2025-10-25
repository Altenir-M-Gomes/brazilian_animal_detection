import { Card, CardContent } from "@/components/ui/card";
import { Upload, FolderOpen, Download } from "lucide-react";
import Header from "@/components/Header";
import { useRef, useState } from "react";
import { toast } from "react-toastify";
import JSZip from "jszip";
import { saveAs } from "file-saver";

export default function PrevisaoScreen() {
  const fileInputRef = useRef(null);
  const folderInputRef = useRef(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [results, setResults] = useState({ animais: [], naoAnimais: [] });

  const getToken = () => localStorage.getItem("token");

  const handleCardClick = () => fileInputRef.current?.click();
  const handleFolderClick = () => folderInputRef.current?.click();

  const handleFileChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setImagePreview(URL.createObjectURL(file));
    setPredictionResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/predict`, {
        method: "POST",
        headers: { Authorization: `Bearer ${getToken()}` },
        body: formData,
      });

      if (!response.ok) throw new Error(`Erro: ${response.status}`);
      const data = await response.json();

      const isAnimal = data.classe_prevista === 1;
      setPredictionResult(isAnimal ? "Contém animal 🐾" : "Não contém animal 🚫");
      toast.success("Classificação concluída!");
    } catch (err) {
      console.error("❌ Erro ao enviar imagem:", err);
      toast.error(err.message || "Erro ao enviar imagem");
    }
  };

  const handleFolderChange = async (event) => {
    const files = Array.from(event.target.files);
    if (files.length === 0) return;

    setResults({ animais: [], naoAnimais: [] });
    toast.loading("Processando imagens...");

    const animais = [];
    const naoAnimais = [];

    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch(`${import.meta.env.VITE_API_URL}/predict`, {
          method: "POST",
          headers: { Authorization: `Bearer ${getToken()}` },
          body: formData,
        });

        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        const data = await response.json();

        const isAnimal = data.classe_prevista === 1;
        if (isAnimal) {
          animais.push({ name: file.name, blob: file });
        } else {
          naoAnimais.push({ name: file.name, blob: file });
        }
      }

      toast.dismiss();
      setResults({ animais, naoAnimais });
      toast.success("Classificação concluída!");
    } catch (err) {
      toast.dismiss();
      console.error("❌ Falha ao enviar pasta:", err);
      toast.error(err.message || "Erro ao enviar pasta");
    }
  };

  const handleDownload = async (files, nomeZip) => {
    if (!files || files.length === 0) {
      toast.warning("Nenhuma imagem para baixar !");
      return;
    }

    const zip = new JSZip();

    try {
      toast.info(`Gerando ${nomeZip}...`);

      for (const file of files) {
        zip.file(file.name, file.blob);
      }

      const zipBlob = await zip.generateAsync({ type: "blob" });
      saveAs(zipBlob, nomeZip);

      toast.success(`${nomeZip} baixado com sucesso!`);
    } catch (err) {
      console.error("❌ Erro ao gerar ZIP:", err);
      toast.error("Erro ao gerar o ZIP");
    }
  };

  const handleReset = () => {
    setImagePreview(null);
    setPredictionResult(null);
    setResults({ animais: [], naoAnimais: [] });
  };

  return (
    <div>
      <Header />
      <div className="flex flex-col justify-center items-center min-h-screen gap-6 p-4">
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

        {!imagePreview && results.animais.length === 0 && results.naoAnimais.length === 0 ? (
          <Card
            onClick={handleCardClick}
            className="w-full max-w-5xl h-[60vh] flex flex-col items-center justify-center border border-gray-400 cursor-pointer hover:bg-gray-50 transition"
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
        ) : null}

        {imagePreview && (
          <div className="flex flex-col items-center">
            {predictionResult && (
              <h2 className="text-xl font-semibold mb-2">{predictionResult}</h2>
            )}
            <img
              src={imagePreview}
              alt="Pré-visualização"
              className="max-h-80 rounded-lg shadow-md"
            />
            <button
              onClick={handleReset}
              className="mt-4 text-sm text-blue-600 hover:underline"
            >
              Nova previsão
            </button>
          </div>
        )}

        {(results.animais.length > 0 || results.naoAnimais.length > 0) && (
          <div className="w-full max-w-5xl mt-4">
            <div className="flex justify-center gap-4 mb-4">
              <button
                onClick={() => handleDownload(results.animais, "animais.zip")}
                className="flex items-center gap-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-xl"
              >
                <Download className="w-4 h-4" /> Baixar animais
              </button>

              <button
                onClick={() => handleDownload(results.naoAnimais, "nao_animais.zip")}
                className="flex items-center gap-2 bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-xl"
              >
                <Download className="w-4 h-4" /> Baixar não animais
              </button>
            </div>

            <div className="flex justify-center mt-10">
              <button
                onClick={handleReset}
                className="text-blue-600 text-sm hover:underline"
              >
                Nova previsão
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
