<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { Head, useForm } from '@inertiajs/vue3';
import PrimaryButton from '@/Components/PrimaryButton.vue';

// Define as propriedades que o Controller pode nos enviar
defineProps({
    resultado: {
        type: String,
        default: '',
    },
});

// Cria o formulário
const form = useForm({
    ticker: '',
});

// Função de envio
const submit = () => {
    form.post(route('analysis.store'));
};
</script>

<template>
    <Head title="Análise Financeira" />

    <AuthenticatedLayout>
        <template #header>
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">Painel de Análise Financeira</h2>
        </template>

        <div class="py-12">
            <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                    <div class="p-6 text-gray-900">

                        <form @submit.prevent="submit" class="space-y-4">
                            <div>
                                <label for="ticker" class="block text-sm font-medium text-gray-700">
                                    Digite o Ticker da Ação (ex: AAPL, MSFT):
                                </label>
                                <input
                                    type="text"
                                    id="ticker"
                                    v-model="form.ticker"
                                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                                    required
                                />
                            </div>

                            <PrimaryButton :disabled="form.processing">
                                Iniciar Análise
                            </PrimaryButton>
                        </form>

                        <!-- 
                            O ERRO ESTAVA AQUI:
                            'vVite-if' (ERRADO) foi corrigido para 'v-if' (CORRETO).
                        -->
                        <div v-if="resultado" class="mt-6 p-4 bg-gray-100 rounded-md">
                            <h3 class="font-semibold">Resultado da Análise:</h3>
                            
                            <!-- 
                                A CORREÇÃO DO TEXTO CORTADO ESTÁ AQUI:
                                1. Tag <div>
                                2. Classe 'whitespace-pre-wrap' (para quebrar a linha)
                            -->
                            <div class="mt-2 text-sm text-gray-700 whitespace-pre-wrap">{{ resultado }}</div>
                        
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>