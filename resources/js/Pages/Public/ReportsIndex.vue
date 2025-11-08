<script setup>
import { Head, Link } from '@inertiajs/vue3';
import ApplicationLogo from '@/Components/ApplicationLogo.vue'; // Adicionamos o Logo

defineProps({
    reports: Array,
});
</script>

<template>
    <Head title="Relatórios Públicos" />

   
    <div class="min-h-screen bg-gray-100">
        <!-- Navegação Pública Simples -->
        <nav class="bg-white border-b border-gray-100">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex">
                        <!-- Logo -->
                        <div class="shrink-0 flex items-center">
                            <Link :href="route('welcome')">
                                <ApplicationLogo class="block h-9 w-auto fill-current text-gray-800" />
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <!-- Conteúdo da Página -->
        <main>
           
            <div class="w-full max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
                
                <h1 class="text-3xl font-bold text-center text-gray-800 mb-8">
                    Análises Financeiras
                </h1>

                <!-- Se a lista estiver vazia -->
                <div v-if="!reports.length" class="text-center text-gray-500 bg-white p-6 rounded-lg shadow-sm">
                    <p class="text-lg">Ainda não há relatórios aprovados para exibição.</p>
                </div>

                <!-- Se a lista NÃO estiver vazia -->
                <div v-else class="space-y-6">
                    <Link 
                        v-for="report in reports" 
                        :key="report.id" 
                        :href="route('reports.public.show', report.id)"
                        class="block p-6 sm:p-8 bg-white shadow-sm sm:rounded-lg hover:shadow-md transition-shadow duration-200"
                    >
                        <article>
                            <h2 class="text-2xl font-semibold text-indigo-700 hover:text-indigo-900">
                                Relatório de Análise: {{ report.ticker }}
                            </h2>
                            <p class="text-sm text-gray-500 mt-2">
                                Publicado em: {{ new Date(report.updated_at).toLocaleDateString('pt-BR', { timeZone: 'UTC' }) }}
                            </p>
                            <p class="text-gray-600 mt-4 line-clamp-2">
                                {{ report.report_final_human.substring(0, 150) }}...
                            </p>
                        </article>
                    </Link> 
                </div> 
            </div> 
        </main>
    </div>
</template>