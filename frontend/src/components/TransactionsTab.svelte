<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let transactions = [];
  let loading = true;
  let error = null;

  // Filters
  let startDate = '';
  let endDate = '';
  let uncategorizedOnly = false;

  // Debouncing for filters
  let filterTimeout;

  onMount(() => {
    // Set default dates (current month)
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    startDate = firstDay.toISOString().split('T')[0];
    endDate = lastDay.toISOString().split('T')[0];
    
    fetchTransactions();
  });

  async function fetchTransactions() {
    loading = true;
    error = null;
    try {
      let url = `/api/transactions?`;
      if (startDate) url += `start=${startDate}&`;
      if (endDate) url += `end=${endDate}&`;
      if (uncategorizedOnly) url += `uncategorized_only=true&`;

      const response = await axios.get(url);
      if (response.data && response.data.length > 0 && response.data[0].error) {
        throw new Error(response.data[0].error);
      }
      transactions = response.data;
    } catch (err) {
      error = err.message || "Error al cargar las transacciones";
    } finally {
      loading = false;
    }
  }

  function handleFilterChange() {
    clearTimeout(filterTimeout);
    filterTimeout = setTimeout(() => {
      fetchTransactions();
    }, 500);
  }

  function formatCurrency(value, type) {
    const formatted = new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(Math.abs(value));

    if (type === 'deposit') return `+ ${formatted}`;
    if (type === 'withdrawal') return `- ${formatted}`;
    return formatted;
  }

  function formatDate(dateStr) {
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
  }

  function getTypeColor(type) {
    if (type === 'deposit') return 'text-emerald-400';
    if (type === 'withdrawal') return 'text-red-400';
    return 'text-slate-400'; // transfers
  }

  function getTypeIcon(type) {
    if (type === 'deposit') {
      return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 11l5-5m0 0l5 5m-5-5v12" /></svg>`;
    } else if (type === 'withdrawal') {
      return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 13l-5 5m0 0l-5-5m5 5V6" /></svg>`;
    } else {
      return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>`;
    }
  }
</script>

<div class="space-y-6 animate-fade-in">
  <!-- Filters Header -->
  <div class="bg-dark-card border border-dark-border rounded-3xl p-5 shadow-lg space-y-4">
    <div class="flex items-center justify-between border-b border-dark-border/50 pb-3 mb-2">
      <h2 class="text-lg font-semibold text-white">Filtros</h2>
      
      <!-- Toggle Uncategorized -->
      <label class="flex items-center cursor-pointer group">
        <div class="relative">
          <input type="checkbox" class="sr-only" bind:checked={uncategorizedOnly} on:change={handleFilterChange}>
          <div class="block w-10 h-6 bg-dark-bg border border-dark-border rounded-full transition-colors group-hover:border-brand/50 {uncategorizedOnly ? 'bg-brand/20 border-brand' : ''}"></div>
          <div class="dot absolute left-1 top-1 bg-slate-400 w-4 h-4 rounded-full transition {uncategorizedOnly ? 'transform translate-x-4 bg-brand' : ''}"></div>
        </div>
        <div class="ml-3 text-sm font-medium text-slate-300">Sin Categoría</div>
      </label>
    </div>

    <!-- Date Pickers -->
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-xs text-slate-500 mb-1" for="startDate">Desde</label>
        <input type="date" id="startDate" bind:value={startDate} on:change={handleFilterChange} 
          class="w-full bg-dark-bg border border-dark-border rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-brand/50">
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1" for="endDate">Hasta</label>
        <input type="date" id="endDate" bind:value={endDate} on:change={handleFilterChange} 
          class="w-full bg-dark-bg border border-dark-border rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-brand/50">
      </div>
    </div>
  </div>

  {#if error}
    <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 text-red-400 text-sm">
      {error}
    </div>
  {/if}

  <!-- Transactions List -->
  <div class="bg-dark-card border border-dark-border rounded-3xl overflow-hidden shadow-lg">
    {#if loading}
      <div class="p-8 text-center text-slate-500 animate-pulse">Cargando transacciones...</div>
    {:else if transactions.length === 0}
      <div class="p-8 text-center text-slate-500 flex flex-col items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-slate-600 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        No se encontraron movimientos.
      </div>
    {:else}
      <div class="divide-y divide-dark-border/50">
        {#each transactions as tx}
          <div class="p-4 flex items-center justify-between hover:bg-dark-surface/50 transition-colors">
            
            <div class="flex items-center gap-4 overflow-hidden">
              <!-- Icon Base -->
              <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center 
                {tx.type === 'deposit' ? 'bg-emerald-500/10 text-emerald-400' : 
                 tx.type === 'withdrawal' ? 'bg-red-500/10 text-red-400' : 'bg-slate-500/10 text-slate-400'}">
                {@html getTypeIcon(tx.type)}
              </div>
              
              <!-- Details -->
              <div class="min-w-0 pr-4">
                <p class="text-sm font-medium text-slate-200 truncate" title={tx.description}>
                  {tx.description}
                </p>
                <div class="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                  <span class="whitespace-nowrap">{formatDate(tx.date)}</span>
                  <span>&bull;</span>
                  <span class="truncate max-w-[120px] text-slate-400" title={tx.category || 'Sin categoría'}>
                    {tx.category || 'Sin categoría'}
                  </span>
                </div>
              </div>
            </div>

            <!-- Amount -->
            <div class="flex-shrink-0 text-right">
              <div class="text-base font-bold whitespace-nowrap {getTypeColor(tx.type)}">
                {formatCurrency(tx.amount, tx.type)}
              </div>
            </div>

          </div>
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .dot {
    transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
  }
  .animate-fade-in {
    animation: fadeIn 0.4s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
