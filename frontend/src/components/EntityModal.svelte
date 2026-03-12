<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import axios from 'axios';
  import TransactionList from './TransactionList.svelte';

  export let filterType = ''; // 'category', 'tag', 'source', 'destination'
  export let filterValue = '';

  const dispatch = createEventDispatcher();
  
  let transactions = [];
  let loading = true;
  let error = null;

  let totals = {
    income: 0,
    expense: 0,
    net: 0
  };

  // Reactive statement to re-fetch when filter arguments change
  $: if (filterType && filterValue) {
    fetchData(filterType, filterValue);
  }

  async function fetchData(type, value) {
    loading = true;
    error = null;
    try {
      const url = `/api/transactions?${type}=${encodeURIComponent(value)}`;
      const response = await axios.get(url);
      
      if (response.data && response.data.length > 0 && response.data[0].error) {
        throw new Error(response.data[0].error);
      }
      
      transactions = response.data;
      
      // Calculate totals
      totals.income = 0;
      totals.expense = 0;
      
      transactions.forEach(tx => {
        if (tx.type === 'deposit') totals.income += tx.amount;
        if (tx.type === 'withdrawal') totals.expense += tx.amount;
      });
      totals.net = totals.income - totals.expense;

    } catch (err) {
      error = err.message || "Error al cargar los datos";
    } finally {
      loading = false;
    }
  }

  function formatCurrency(value) {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(Math.abs(value));
  }

  function getTitle() {
    switch (filterType) {
      case 'category': return 'Categoría';
      case 'tag': return 'Etiqueta';
      case 'source': return 'Cuenta Origen';
      case 'destination': return 'Cuenta Destino';
      default: return 'Filtro';
    }
  }

  function handleClose() {
    dispatch('close');
  }
</script>

<div class="fixed inset-0 z-[200] flex items-end sm:items-center justify-center sm:p-4 bg-black/80 backdrop-blur-sm animate-fade-in" on:click={handleClose} on:keydown={(e) => e.key === 'Escape' && handleClose()} role="dialog" tabindex="-1">
  <div class="bg-dark-bg border border-dark-border rounded-t-3xl sm:rounded-3xl w-full max-w-2xl sm:max-h-[85vh] h-[90vh] sm:h-auto shadow-2xl flex flex-col overflow-hidden animate-slide-up" on:click|stopPropagation role="document">
    
    <!-- Header -->
    <div class="px-6 py-4 border-b border-dark-border flex justify-between items-center bg-dark-surface sticky top-0 z-10">
      <div>
        <span class="text-xs uppercase tracking-widest text-slate-500 font-semibold">{getTitle()}</span>
        <h2 class="text-xl font-bold text-white mt-1 flex items-center gap-2">
          {#if filterType === 'tag'}
            <span class="text-brand">#</span>
          {/if}
          {filterValue}
        </h2>
      </div>
      <button on:click={handleClose} class="p-2 bg-dark-card rounded-full text-slate-400 hover:text-white hover:bg-dark-border transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Scrollable Content -->
    <div class="overflow-y-auto flex-1 p-4 sm:p-6 space-y-6 custom-scrollbar">
      
      {#if error}
        <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 text-red-400 text-sm">
          {error}
        </div>
      {/if}

      <!-- Totals Hero -->
      {#if !loading && !error}
        <div class="grid grid-cols-3 gap-3">
          <div class="bg-dark-card border border-dark-border rounded-2xl p-4 flex flex-col justify-center text-center">
            <span class="text-xs text-slate-500 mb-1">Ingresos</span>
            <span class="text-lg font-bold text-emerald-400">+{formatCurrency(totals.income)}</span>
          </div>
          <div class="bg-dark-card border border-dark-border rounded-2xl p-4 flex flex-col justify-center text-center">
            <span class="text-xs text-slate-500 mb-1">Gastos</span>
            <span class="text-lg font-bold text-red-400">-{formatCurrency(totals.expense)}</span>
          </div>
          <div class="bg-gradient-to-br from-dark-surface to-dark-card border border-brand/30 rounded-2xl p-4 flex flex-col justify-center text-center">
            <span class="text-xs text-slate-500 mb-1">Balance</span>
            <span class="text-lg font-bold {totals.net >= 0 ? 'text-white' : 'text-red-400'}">
              {totals.net >= 0 ? '+' : '-'}{formatCurrency(totals.net)}
            </span>
          </div>
        </div>
      {/if}

      <!-- Transaction List -->
      <div class="bg-dark-bg rounded-3xl">
        <TransactionList 
          {transactions} 
          {loading} 
          on:drilldown={(e) => {
            // If they click another drilldown inside the modal, we update our own state to drill further!
            filterType = e.detail.type;
            filterValue = e.detail.value;
            // The onMount effect won't re-run automatically on prop change unless we put the fetch in a reactive block
            // However, Svelte 3 component regeneration is easier:
          }}
        />
      </div>

    </div>
  </div>
</div>

<style>
  .animate-fade-in {
    animation: fadeIn 0.3s ease-out;
  }
  .animate-slide-up {
    animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  @keyframes slideUp {
    from { opacity: 0; transform: translateY(40px) scale(0.98); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  
  .custom-scrollbar::-webkit-scrollbar {
    width: 6px;
  }
  .custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
  }
  .custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
  }
</style>
