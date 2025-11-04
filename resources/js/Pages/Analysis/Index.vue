<script setup>
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout.vue';
import { Head, useForm } from '@inertiajs/vue3';
import PrimaryButton from '@/Components/PrimaryButton.vue';

// Isso define as propriedades que o Controller pode nos enviar
// (Lembra do '$resultado'?)
defineProps({
    resultado: {
        type: String,
        default: '',
    },
});

// Isso cria o nosso formulário
const form = useForm({
    ticker: '', // O campo para o nome da ação
});

// Esta função será chamada quando o formulário for enviado
const submit = () => {
    // Envia o formulário para a rota 'analysis.store' (o método POST)
    form.post(route('analysis.store'), {
        // Não faz nada quando terminar (apenas recarrega a página com o resultado)
    });
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

                        <div v-if="resultado" class="mt-6 p-4 bg-gray-100 rounded-md">
                            <h3 class="font-semibold">Resultado da Análise:</h3>
                            <pre class="mt-2 text-sm text-gray-700">{{ resultado }}</pre>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </AuthenticatedLayout>
</template>