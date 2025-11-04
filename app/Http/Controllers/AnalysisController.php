<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;
use Illuminate\Support\Facades\Http; 
use App\Models\Report; // <--- 1. IMPORTE O NOVO MODEL

class AnalysisController extends Controller
{
    public function index()
    {
        return Inertia::render('Analysis/Index');
    }

    public function store(Request $request)
    {
        $ticker = $request->input('ticker');

        try {
            $response = Http::timeout(300)
                ->post('http://python:8000/analyze-stock', [
                    'stock_symbol' => $ticker,
                ]);

            $data = $response->json();

            if ($response->failed()) {
                $errorMessage = $data['detail']['message'] ?? $data['detail'] ?? 'Erro desconhecido no backend Python.';
                throw new \Exception($errorMessage);
            }

            // --- 2. SALVE O RELATÓRIO NO BANCO DE DADOS ---
            $report = Report::create([
                'ticker' => $ticker,
                'report_draft_ai' => $data['message'], // Salva o rascunho da IA
                'status' => 'pending_review' // Define o status inicial
            ]);

            // 3. PASSE O RASCUNHO PARA A VIEW
            // (No futuro, podemos redirecionar para o "Painel de Curadoria")
            $resultado = $report->report_draft_ai;

        } catch (\Exception $e) {
            $resultado = "ERRO AO EXECUTAR A ANÁLISE: " . $e->getMessage();
        } 

        return Inertia::render('Analysis/Index', [
            'resultado' => $resultado
        ]);
    }
}