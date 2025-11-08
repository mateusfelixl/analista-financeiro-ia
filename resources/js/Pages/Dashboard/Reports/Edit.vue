<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import PrimaryButton from '@/Components/PrimaryButton.vue';
import { Head, useForm } from '@inertiajs/vue3';
import { defineProps } from 'vue';

// O ReportController (método 'edit') está nos enviando o 'report' completo.
const props = defineProps({
    report: Object,
});

// --- A MELHORIA ESTÁ AQUI ---
// Em vez de um formulário vazio, nós o inicializamos (pré-preenchemos)
// com os dados que o 'report' nos enviou.
const form = useForm({
    // O campo 'report_final_human' começa com o rascunho da IA.
    report_final_human: props.report.report_draft_ai, 
    
    // O campo 'human_notes' começa com qualquer nota que já exista (ou vazio).
    human_notes: props.report.human_notes || '', 
});
// --- FIM DA MELHORIA ---


// A função de "Salvar"
const submit = () => {
    // Envia o formulário (com os dados editados) para a rota 'update'.
    form.put(route('reports.update', props.report.id));
};
</script>

<template>
    <Head :title="'Revisar Relatório: ' + report.ticker" />

    <AuthenticatedLayout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Revisando Relatório: {{ report.ticker }}
            </h2>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6 text-gray-900">
                        
                        <!-- Formulário que chama a função 'submit' -->
                        <form @submit.prevent="submit">
                            
                            <!-- 
                                CAMPO 1: O RASCUNHO FINAL (EDITÁVEL)
                                Agora pré-preenchido com o rascunho da IA.
                            -->
                            <div>
                                <label for="report_final_human" class="block text-sm font-medium text-gray-700">
                                    Relatório Final (Editável)
                                </label>
                                <textarea
                                    id="report_final_human"
                                    v-model="form.report_final_human"
                                    rows="20"
                                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 font-mono text-sm"
                                ></textarea>
                                <!-- Mostra erro se o campo for enviado vazio -->
                                <p v-if="form.errors.report_final_human" class="text-sm text-red-600 mt-1">
                                    {{ form.errors.report_final_human }}
                                </p>
                            </div>

                            <!-- CAMPO 2: NOTAS INTERNAS (OPCIONAL) -->
                            <div class="mt-6">
                                <label for="human_notes" class="block text-sm font-medium text-gray-700">
                                    Notas Internas do Revisor (Opcional)
                                </label>
                                <textarea
                                    id="human_notes"
                                    v-model="form.human_notes"
                                    rows="3"
                                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
                                    placeholder="Ex: IA esqueceu de mencionar o P/L."
                                ></textarea>
                            </div>

                            <!-- Botão de "Salvar" -->
                            <div class="flex items-center justify-end mt-6">
                                <PrimaryButton :disabled="form.processing">
                                    Aprovar e Publicar
                                </PrimaryButton>
                            </div>
                        </form>

                    </div>
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>