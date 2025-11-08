<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

// O nome da classe é anônimo, o que é o padrão moderno do Laravel
return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * (Este método é executado quando você roda 'php artisan migrate')
     */
    public function up(): void
    {
        // Nós usamos Schema::table (para alterar) e NÃO Schema::create (para criar)
        Schema::table('reports', function (Blueprint $table) {
            
            // Esta é a linha mágica que corrige o bug do "texto cortado"
            // Ela muda a coluna 'report_draft_ai' de VARCHAR(255) para LONGTEXT
            $table->longText('report_draft_ai')->change();
        });
    }

    /**
     * Reverse the migrations.
     *
     * (Este método é executado quando você roda 'php artisan migrate:rollback')
     */
    public function down(): void
    {
        Schema::table('reports', function (Blueprint $table) {
            
            // Esta linha reverte a mudança, caso precisemos
            $table->string('report_draft_ai')->change();
        });
    }
};