<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { Head, Link } from '@inertiajs/vue3';

// Isso "recebe" a lista de 'reports' que o seu ReportController (PHP) enviou
defineProps({
    reports: Array, // Espera um array (lista) de relatórios
});
</script>

<template>
    <Head title="Painel de Curadoria" />

    <AuthenticatedLayout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">Painel de Curadoria</h2>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6 text-gray-900">
                        
                        <!-- Título da Página -->
                        <h3 class="text-lg font-medium text-gray-900 mb-4">Relatórios Pendentes de Revisão</h3>

                        <!-- Tabela para listar os relatórios -->
                        <div class="border rounded-lg overflow-hidden">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ticker</th>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data da Análise</th>
                                        <!-- Deixamos um espaço para o botão "Revisar" no futuro -->
                                        <th scope="col" class="relative px-6 py-3"><span class="sr-only">Ações</span></th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    
                                    <!-- Loop (v-for) para cada relatório pendente -->
                                    <tr v-for="report in reports" :key="report.id">
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ report.ticker }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            <!-- Um "badge" (etiqueta) bonito para o status -->
                                            <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                                {{ report.status }}
                                            </span>
                                        </td>
                                        <!-- Formata a data para um formato legível (ex: 07/11/2025 22:30:10) -->
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ new Date(report.created_at).toLocaleString('pt-BR') }}</td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            
                                             <Link :href="route('reports.edit', report.id)" class="text-indigo-600 hover:text-indigo-900">Revisar</Link> 
                                        </td>
                                    </tr>

                                    <!-- Mensagem inteligente se a lista estiver vazia -->
                                    <tr v-if="reports.length === 0">
                                        <td colspan="4" class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 text-center">
                                            Nenhum relatório pendente de revisão. Gere uma nova análise na página "Análise"!
                                        </td>
                                    </tr>

                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>