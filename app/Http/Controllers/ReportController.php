<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Inertia\Inertia;      // Importa o Inertia (para renderizar o Vue)
use App\Models\Report;    // Importa o "molde" do Relatório (para buscar no banco)
use Exception; // Importa a classe base de Exceção

class ReportController extends Controller
{
    /**
     * PASSO 1: Exibe a lista de relatórios pendentes de revisão.
     * (Controla o painel /dashboard/reports)
     */
    public function index()
    {
        // 1. Busca no banco de dados TODOS os relatórios
        //    que estão com o status 'pending_review'
        //    e ordena pelos mais recentes primeiro.
        $pendingReports = Report::where('status', 'pending_review')
                                ->latest() // 'latest()' é o mesmo que 'orderBy('created_at', 'DESC')'
                                ->get();

        // 2. Envia os relatórios encontrados para a sua página Vue 'Index.vue'
        return Inertia::render('Dashboard/Reports/Index', [
            'reports' => $pendingReports, // Envia a lista como uma "prop" chamada 'reports'
        ]);
    }

    /**
     * PASSO 2: Mostra a página de edição para um relatório específico.
     * (Controla o clique no botão "Revisar")
     */
    public function edit(Report $report)
    {
        // 1. O Laravel busca automaticamente o relatório pelo ID
        //    (graças ao 'Type Hinting' -> Report $report)

        // 2. Renderiza a página de EDIÇÃO (o arquivo 'Edit.vue' 
        //    que você criou) e envia o relatório para ela.
        return Inertia::render('Dashboard/Reports/Edit', [
            'report' => $report,
        ]);
    }

    /**
     * PASSO 3: Atualiza o relatório no banco de dados.
     * (Controla o clique no botão "Aprovar e Publicar")
     */
    public function update(Request $request, Report $report)
    {
        // 1. Validação (garante que o relatório final não esteja vazio)
        $validatedData = $request->validate([
            'report_final_human' => 'required|string',
            'human_notes' => 'nullable|string',
        ]);

        // 2. Atualiza o relatório no banco com os dados do formulário
        $report->update([
            'report_final_human' => $validatedData['report_final_human'],
            'human_notes' => $validatedData['human_notes'],
            'status' => 'approved' // Muda o status para "Aprovado"!
        ]);

        // 3. Redireciona o usuário de volta para o Painel de Curadoria
        //    com uma mensagem de sucesso.
        return redirect()->route('reports.index')->with('success', 'Relatório aprovado com sucesso!');
    }

    /**
     * PASSO 4: Exibe a lista PÚBLICA de relatórios APROVADOS.
     * (Controla a página /relatorios que acabamos de criar)
     */
    public function showPublicList()
    {
        // 1. Busca no banco de dados TODOS os relatórios
        //    que estão com o status 'approved'
        //    e ordena pelos mais recentes primeiro.
        $approvedReports = Report::where('status', 'approved')
                                    ->latest()
                                    ->get();

        // 2. Envia os relatórios encontrados para a nova página Vue 'Public/ReportsIndex'
        return Inertia::render('Public/ReportsIndex', [
            'reports' => $approvedReports,
        ]);
    }

      /**
     * PASSO 5: Exibe a página PÚBLICA de UM relatório APROVADO.
     * (Controla a página /relatorios/{id})
     */
    public function showPublicReport(Report $report)
    {

        // 2. VERIFICAÇÃO DE SEGURANÇA:
        if ($report->status !== 'approved') {
            abort(404); 
        }

        // 3. Envia o relatório encontrado para uma nova página Vue
        return \Inertia\Inertia::render('Public/ReportShow', [
            'report' => $report,
        ]);
    }
}
