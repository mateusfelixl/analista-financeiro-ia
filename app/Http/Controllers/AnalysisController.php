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
        return Inertia::render('Analysis/Index');
    }

    /**
     * Processa a solicitação de análise (o formulário).
     */
    public function store(Request $request)
    {
        // Valida se o ticker foi enviado
        $request->validate([
            'ticker' => 'required|string|max:10',
        ]);

        $ticker = $request->input('ticker'); // 1. Pega o 'AAPL'

        try {
            // 2. CHAMA A API DO PYTHON
            $response = Http::timeout(300) 
                 ->post('http://python:8000/analyze-stock', [
                    'symbol' => $ticker, 
                ]);

            $data = $response->json();

            if ($response->failed()) {
                $errorMessage = $data['detail']['message'] ?? null;

                if (!$errorMessage) {
                    $detail = $data['detail'] ?? 'Erro desconhecido';
                    
                    if (is_array($detail)) {
                        $errorMessage = json_encode($detail, JSON_UNESCAPED_UNICODE);
                    } else {
                        $errorMessage = (string) $detail;
                    }
                }

                throw new Exception($errorMessage);
            }

            // --- 5. LIMPAR A "SUJEIRA" DA IA  ---
            $raw_report = $data['message']; // Pega o rascunho bruto (com "Thought:...")
            
            // Procura pelo início do relatório real, que começa com "# Relatório"
            $clean_report = strstr($raw_report, '# Relatório'); 

            // Se (por algum motivo) não encontrar o início, usa o texto bruto
            // para não salvar um rascunho vazio no banco.
            if ($clean_report === false) {
                $clean_report = $raw_report;
            }
            // --- FIM DA LIMPEZA ---


            // 6. SALVE O RELATÓRIO "LIMPO" NO BANCO DE DADOS
            $report = Report::create([
                'ticker' => $ticker,
                'report_draft_ai' => $clean_report, // Salva o rascunho LIMPO
                'status' => 'pending_review' 
            ]);
            
            // 7. PASSE O RASCUNHO LIMPO PARA A VIEW
            $resultado = $report->report_draft_ai;

        } catch (Exception $e) {
            $resultado = "ERRO AO EXECUTAR A ANÁLISE: " . $e->getMessage();
        } 

        // 8. Retorna o resultado (o relatório ou o erro) para a view
        return Inertia::render('Analysis/Index', [
            'resultado' => $resultado
        ]);
    }
}