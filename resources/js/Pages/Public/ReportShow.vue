<script setup>
import { Head, Link } from '@inertiajs/vue3';
import ApplicationLogo from '@/Components/ApplicationLogo.vue'; 
import { computed } from 'vue'; 
import { marked } from 'marked';   

// O ReportController (showPublicReport) está nos enviando o 'report' APROVADO
const props = defineProps({
    report: Object,
});

// A "mágica" do Markdown (que já tínhamos)
const renderedHtml = computed(() => {
    if (props.report && props.report.report_final_human) {
        return marked(props.report.report_final_human);
    }
    return ''; 
});
</script>

<template>
    <Head :title="'Relatório: ' + report.ticker" />

    <!-- 
      Layout de tela cheia (largo) que já fizemos
    -->
    <div class="min-h-screen bg-gray-100">
        <!-- Navegação Pública Simples -->
        <nav class="bg-white border-b border-gray-100">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex">
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

                <article class="p-6 sm:p-8 bg-white shadow-sm sm:rounded-lg">
                    
                    <h1 class="text-3xl font-bold text-gray-900">
                        Relatório de Análise: {{ report.ticker }}
                    </h1>
                    <p class="text-sm text-gray-500 mb-6 border-b pb-4">
                        Publicado em: {{ new Date(report.updated_at).toLocaleDateString('pt-BR', { timeZone: 'UTC' }) }}
                    </p>

                    <!-- 
                      --- A MELHORIA VISUAL 
                    -->
                    <div 
                        v-html="renderedHtml" 
                        class="prose prose-lg max-w-none font-sans text-gray-700 leading-relaxed"
                    >
                        <!-- O v-html vai preencher este div com o HTML "bonito" -->
                    </div>

                    <!-- O link de "Voltar" -->
                    <div class="mt-8 border-t pt-6">
                        <Link 
                            :href="route('reports.public.index')" 
                            class="text-indigo-600 hover:text-indigo-900 font-medium"
                        >
                            &larr; Voltar para todos os relatórios
                        </Link>
                    </div>

                </article>

            </div>
        </main>
    </div>
</template>