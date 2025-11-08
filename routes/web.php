<?php

use App\Http\Controllers\AnalysisController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\ReportController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/


Route::get('/', function () {
    return Inertia::render('Welcome', [
        'canLogin' => Route::has('login'),
        'canRegister' => Route::has('register'),
        'laravelVersion' => Illuminate\Foundation\Application::VERSION,
        'phpVersion' => PHP_VERSION,
    ]);
})->name('welcome'); 

Route::get('/dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

// Esta rota é para os visitantes verem os relatórios APROVADOS.
Route::get('/relatorios', [ReportController::class, 'showPublicList'])
     ->name('reports.public.index'); 

     // Rota da PÁGINA DE DETALHES PÚBLICA
// O {report} é o ID do relatório (ex: 1, 2, 3)
Route::get('/relatorios/{report}', [App\Http\Controllers\ReportController::class, 'showPublicReport'])
     ->name('reports.public.show'); 

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
    // Rota para mostrar a página de análise (GET)
Route::get('/analysis', [AnalysisController::class, 'index'])->name('analysis.index');

// Rota para processar o formulário de análise (POST)
Route::post('/analysis', [AnalysisController::class, 'store'])->name('analysis.store');
});

// Esta será a rota "Painel de Curadoria"
Route::get('/dashboard/reports', [ReportController::class, 'index'])
     ->name('reports.index') // Dá um "apelido" para a rota
     ->middleware(['auth', 'verified']);
     
     // Rota para a página de EDIÇÃO (onde o humano revisa)
Route::get('/dashboard/reports/{report}/edit', [ReportController::class, 'edit'])
     ->name('reports.edit') // O 'apelido' que o botão 'Revisar' está procurando
     ->middleware(['auth', 'verified']);
     
// Rota que "recebe" o formulário da página de Edição
Route::put('/dashboard/reports/{report}', [ReportController::class, 'update'])
     ->name('reports.update') // O 'apelido' que o botão "Aprovar e Publicar" está procurando
     ->middleware(['auth', 'verified']);


require __DIR__.'/auth.php';
