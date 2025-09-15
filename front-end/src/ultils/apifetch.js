import { fetchApi2 } from "./fetchApi";
import { z } from "zod";

// Esquema de validação para a resposta do backend
const RegisterResponseSchema = z.object({
  data: z.object({
    id: z.number(),
    email: z.string(),
  }),
});

/**
 * Função para cadastrar um novo usuário
 * @param {string} email - Email do usuário
 * @param {string} senha - Senha do usuário
 * @returns {Promise<{ id: number, email: string }>} - Dados do usuário cadastrado
 */
export const cadastrarUsuario = async (email, senha) => {
  try {
    const response = await fetchApi2(
      "/api/cadastrar", // Rota do backend
      "POST", // Método HTTP
      { email, senha }, // Dados enviados no corpo da requisição
      null, // Token (não necessário para cadastro)
      RegisterResponseSchema // Esquema de validação Zod
    );

    return response.data; // Retorna os dados do usuário cadastrado
  } catch (error) {
    throw new Error(error.errors?.[0]?.message || "Erro ao cadastrar usuário");
  }
};