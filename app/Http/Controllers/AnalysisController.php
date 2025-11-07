<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Http; 
use App\Models\Report; // Importa o Model do Relatório
use Exception; // Importa a classe base de Exceção

class AnalysisController extends Controller
{
    /**
     * Exibe a página principal de análise.
     */
    public function index()
    {
        // Usa o Inertia para renderizar o componente Vue 'Analysis/Index'
        // (resources/js/Pages/Analysis/Index.vue)
        return Inertia::render('Analysis/Index');
    }

    /**
     * Processa a solicitação de análise (o formulário).
     */
    public function store(Request $request)
    {
        // Valida se o ticker foi enviado (opcional, mas boa prática)
        $request->validate([
            'ticker' => 'required|string|max:10',
        ]);

        $ticker = $request->input('ticker'); // 1. Pega o 'AAPL'

        try {
            // 2. CHAMA A API DO PYTHON
            // Faz a requisição HTTP para o nome do serviço 'python'
            // na porta interna 8000 (exatamente como o nosso teste 'curl' vitorioso)
            $response = Http::timeout(300) // 5 minutos de paciência
                ->post('http://python:8000/analyze-stock', [
                    'stock_symbol' => $ticker,
                ]);

            // 3. Pega a resposta
            $data = $response->json();

            // 4. Se a API do Python deu um erro (ex: 500, 429)
            if ($response->failed()) {
                // Tenta pegar a mensagem de erro da API, senão mostra uma genérica
                $errorMessage = $data['detail']['message'] ?? $data['detail'] ?? 'Erro desconhecido no backend Python.';
                throw new Exception($errorMessage);
            }

            // 5. SALVE O RELATÓRIO NO BANCO DE DADOS
            // (Isso só funciona se a tabela 'reports' existir!)
            $report = Report::create([
                'ticker' => $ticker,
                'report_draft_ai' => $data['message'], // Salva o rascunho da IA
                'status' => 'pending_review' // Define o status inicial
            ]);
            
            // 6. PASSE O RASCUNHO PARA A VIEW
            $resultado = $report->report_draft_ai;

        } catch (Exception $e) {
            // 7. TRATAMENTO DE ERRO LIMPO
            // Se qualquer coisa no 'try' falhar (API, Banco de Dados),
            // captura a mensagem e a envia para o frontend.
            $resultado = "ERRO AO EXECUTAR A ANÁLISE: " . $e->getMessage();
        } 

        // 8. Retorna o resultado (o relatório ou o erro) para a view
        return Inertia::render('Analysis/Index', [
            'resultado' => $resultado
        ]);
    }
}