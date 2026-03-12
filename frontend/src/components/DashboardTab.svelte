<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  import Chart from './Chart.svelte';

  export let startDate;
  export let endDate;
  import HistoryChart from './HistoryChart.svelte';

  let loading = true;
  let error = null;
  let summary = {
    income: 0,
    expenses: 0,
    balance: 0,
    period: { start: '', end: '' }
  };
  let chartData;
  let historyData = [];

  onMount(async () => {
    try {
      const response = await axios.get('/api/summary');
      if (response.data.error) {
        throw new Error(response.data.error);
      }
      summary = response.data;
      
      chartData = {
        labels: ['Ingresos', 'Gastos', 'Balance'],
        datasets: [{
          data: [summary.income, summary.expenses, summary.balance],
          backgroundColor: [
            'rgba(16, 185, 129, 0.8)', // emerald
            'rgba(239, 68, 68, 0.8)',  // red
            'rgba(59, 130, 246, 0.8)', // blue
          ],
          borderRadius: 6,
          borderWidth: 0
        }]
      };
    } catch (err) {
      error = err.message || "Error al cargar el resumen";
      console.error(err);
    } finally {
      loading = false;
    }
  }

  // Function to fetch history data
  async function fetchHistory() {
    try {
      const historyRes = await axios.get('/api/history?months=12'); // Changed to months=12
      historyData = historyRes.data;
    } catch (e) {
      console.error("Failed to load history:", e);
    }
  }

  // Initial data load on mount
  onMount(() => {
    fetchSummary();
    fetchHistory();
  });

  // Re-fetch summary when startDate or endDate changes
  $: if (startDate && endDate) {
    fetchSummary();
  }

  function formatCurrency(value) {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(value);
  }
</script>

<div class="space-y-6">
  {#if error}
    <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 text-red-400 text-sm">
      {error}
    </div>
  {/if}

  {#if loading}
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      {#each Array(3) as _}
        <div class="bg-dark-card rounded-3xl p-6 h-32 animate-pulse flex flex-col justify-center">
          <div class="h-4 bg-dark-border rounded w-1/3 mb-4"></div>
          <div class="h-8 bg-dark-border rounded w-1/2"></div>
        </div>
      {/each}
    </div>
    <div class="bg-dark-card rounded-3xl p-6 h-[400px] animate-pulse mt-6"></div>
  {:else}
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-gradient-to-br from-dark-card to-dark-surface border border-dark-border rounded-3xl p-6 shadow-lg relative overflow-hidden group hover:border-brand-dark transition-colors duration-300">
        <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3" />
          </svg>
        </div>
        <h2 class="text-sm font-medium text-slate-400 mb-2">Balance Total</h2>
        <div class="text-3xl font-bold {summary.balance >= 0 ? 'text-white' : 'text-red-400'}">
          {formatCurrency(summary.balance)}
        </div>
        <div class="text-xs text-slate-500 mt-2">{summary.period.start.slice(0, 7) || 'Actual'}</div>
      </div>

      <div class="bg-dark-card border border-dark-border rounded-3xl p-6 shadow-lg hover:border-dark-border/80 transition-colors">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-sm font-medium text-slate-400">Ingresos</h2>
          <div class="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12" />
            </svg>
          </div>
        </div>
        <div class="text-2xl font-bold text-emerald-400">
          {formatCurrency(summary.income)}
        </div>
      </div>

      <div class="bg-dark-card border border-dark-border rounded-3xl p-6 shadow-lg hover:border-dark-border/80 transition-colors">
        <div class="flex items-center justify-between mb-2">
          <h2 class="text-sm font-medium text-slate-400">Gastos</h2>
          <div class="w-8 h-8 rounded-full bg-red-500/10 flex items-center justify-center text-red-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 13l-5 5m0 0l-5-5m5 5V6" />
            </svg>
          </div>
        </div>
        <div class="text-2xl font-bold text-red-400">
          {formatCurrency(summary.expenses)}
        </div>
      </div>
    </section>

    <section class="bg-dark-card border border-dark-border rounded-3xl p-4 md:p-6 shadow-lg mt-6">
      <div class="h-[300px] md:h-[400px] w-full">
        {#if chartData}
          <Chart data={chartData} type="bar" title="Desglose del Mes Actual" />
        {/if}
      </div>
    </section>

    <section class="bg-dark-card border border-dark-border rounded-3xl p-4 md:p-6 shadow-lg mt-6 mb-12">
      <div class="h-[300px] md:h-[400px] w-full">
        {#if historyData.length > 0}
          <HistoryChart data={historyData} />
        {/if}
      </div>
    </section>
  {/if}
</div>
