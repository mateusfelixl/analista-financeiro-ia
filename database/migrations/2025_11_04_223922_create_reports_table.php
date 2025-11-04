<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('reports', function (Blueprint $table) {
            $table->id();
            
            $table->string('ticker'); // Coluna para salvar o ticker (ex: "AAPL")
            
            // Coluna para o rascunho bruto da IA (usamos 'text' para textos longos)
            $table->text('report_draft_ai'); 
            
            // Coluna para o relatório final, editado pelo humano (pode ser nulo no início)
            $table->text('report_final_human')->nullable(); 

            // Coluna para o status do fluxo de trabalho
            // O padrão será 'pending_review' (pendente de revisão)
            $table->string('status')->default('pending_review'); 
            
            // Coluna opcional para notas do revisor (pode ser nula)
            $table->text('human_notes')->nullable();

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('reports');
    }
};
