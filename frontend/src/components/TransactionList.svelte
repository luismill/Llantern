<script>
  import { createEventDispatcher } from 'svelte';
  import { getCategoryIcon } from '../utils/icons.js';
  
  export let transactions = [];
  export let loading = false;

  const dispatch = createEventDispatcher();
  let selectedTx = null;

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
    if (!dateStr) return '';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
  }

  function getTypeColor(type) {
    if (type === 'deposit') return 'text-emerald-400';
    if (type === 'withdrawal') return 'text-red-400';
    return 'text-slate-400';
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

  function handleFilterClick(type, value) {
    selectedTx = null; // Close modal
    dispatch('drilldown', { type, value });
  }
</script>

<div class="bg-dark-card border border-dark-border rounded-3xl overflow-hidden shadow-lg">
  {#if loading}
    <div class="p-8 text-center text-slate-500 animate-pulse flex flex-col items-center">
      <svg class="animate-spin -ml-1 mr-3 h-8 w-8 text-brand mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Cargando transacciones...
    </div>
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
        <div 
          class="p-4 flex items-center justify-between hover:bg-dark-surface/50 transition-colors cursor-pointer"
          on:click={() => selectedTx = tx}
          on:keydown={(e) => e.key === 'Enter' && (selectedTx = tx)}
          role="button"
          tabindex="0"
        >
          <div class="flex items-center gap-4 overflow-hidden">
            <div class="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center 
              {tx.type === 'deposit' ? 'bg-emerald-500/10 text-emerald-400' : 
               tx.type === 'withdrawal' ? 'bg-red-500/10 text-red-400' : 'bg-slate-500/10 text-slate-400'}">
              {@html getTypeIcon(tx.type)}
            </div>
            
            <div class="min-w-0 pr-4">
              <p class="text-sm font-medium text-slate-200 truncate" title={tx.description}>
                {tx.description}
              </p>
              <div class="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                <span class="whitespace-nowrap">{formatDate(tx.date)}</span>
                <span>&bull;</span>
                <span class="flex items-center gap-1.5 max-w-[140px] text-slate-400" title={tx.category || 'Sin categoría'}>
                  <span class="flex-shrink-0 w-3.5 h-3.5 opacity-80">{@html getCategoryIcon(tx.category)}</span>
                  <span class="truncate">{tx.category || 'Sin categoría'}</span>
                </span>
              </div>
            </div>
          </div>

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

<!-- Transaction Details Modal -->
{#if selectedTx}
  <div class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in" on:click={() => selectedTx = null} on:keydown={(e) => e.key === 'Escape' && (selectedTx = null)} role="dialog" tabindex="-1">
    <div class="bg-dark-card border border-dark-border rounded-3xl w-full max-w-md shadow-2xl overflow-hidden" on:click|stopPropagation role="document">
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-dark-border flex justify-between items-center bg-dark-surface/50">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center 
            {selectedTx.type === 'deposit' ? 'bg-emerald-500/10 text-emerald-400' : 
             selectedTx.type === 'withdrawal' ? 'bg-red-500/10 text-red-400' : 'bg-slate-500/10 text-slate-400'}">
            {@html getTypeIcon(selectedTx.type)}
          </div>
          <h3 class="font-semibold text-white">Detalles del Movimiento</h3>
        </div>
        <button on:click={() => selectedTx = null} class="text-slate-400 hover:text-white transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-4">
        <!-- Amount -->
        <div class="text-center pb-4 border-b border-dark-border/50">
          <div class="text-3xl font-bold {getTypeColor(selectedTx.type)}">
            {formatCurrency(selectedTx.amount, selectedTx.type)}
          </div>
          <p class="text-slate-300 mt-2 font-medium">{selectedTx.description}</p>
        </div>

        <div class="grid grid-cols-2 gap-4 text-sm mt-4">
          <div>
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-1">Fecha</span>
            <span class="text-slate-200 font-medium">{formatDate(selectedTx.date)}</span>
          </div>
          <div>
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-1">Categoría</span>
            <span class="text-slate-200 font-medium">
              {#if selectedTx.category}
                <button 
                  on:click={() => handleFilterClick('category', selectedTx.category)}
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-sm font-medium bg-brand/10 text-brand-light hover:bg-brand/20 transition-colors"
                >
                  <span class="w-4 h-4 opacity-80">{@html getCategoryIcon(selectedTx.category)}</span>
                  <span>{selectedTx.category}</span>
                </button>
              {:else}
                <span class="text-slate-500 italic">Sin categoría</span>
              {/if}
            </span>
          </div>
          <div>
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-1">Origen</span>
            {#if selectedTx.source}
              <button 
                on:click={() => handleFilterClick('account', selectedTx.source)}
                class="text-slate-200 font-medium hover:text-brand-light underline decoration-dark-border hover:decoration-brand-light transition-colors"
              >
                {selectedTx.source}
              </button>
            {:else}
              <span class="text-slate-500 font-medium">-</span>
            {/if}
          </div>
          <div>
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-1">Destino</span>
            {#if selectedTx.destination}
              <button 
                on:click={() => handleFilterClick('account', selectedTx.destination)}
                class="text-slate-200 font-medium hover:text-brand-light underline decoration-dark-border hover:decoration-brand-light transition-colors"
              >
                {selectedTx.destination}
              </button>
            {:else}
              <span class="text-slate-500 font-medium">-</span>
            {/if}
          </div>
        </div>

        <!-- Tags and Notes -->
        {#if selectedTx.tags && selectedTx.tags.length > 0}
          <div class="pt-2">
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-2">Etiquetas</span>
            <div class="flex flex-wrap gap-2">
              {#each selectedTx.tags as tag}
                <button 
                  on:click={() => handleFilterClick('tag', tag)}
                  class="px-2 py-1 bg-dark-bg border border-dark-border text-slate-300 text-xs rounded-md hover:border-brand-light hover:text-brand-light transition-colors"
                >
                  #{tag}
                </button>
              {/each}
            </div>
          </div>
        {/if}
        
        {#if selectedTx.notes}
          <div class="pt-2">
            <span class="block text-slate-500 text-xs uppercase tracking-wider mb-2">Notas</span>
            <p class="text-sm text-slate-300 bg-dark-bg border border-dark-border p-3 rounded-xl whitespace-pre-wrap">{selectedTx.notes}</p>
          </div>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .animate-fade-in {
    animation: fadeIn 0.3s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
  }
</style>
