<script>
  import { onMount } from 'svelte';
  import axios from 'axios';

  let accounts = [];
  let loading = true;
  let error = null;
  let totalBalance = 0;

  onMount(async () => {
    try {
      const response = await axios.get('/api/accounts');
      if (response.data && response.data.length > 0 && response.data[0].error) {
        throw new Error(response.data[0].error);
      }
      accounts = response.data;
      
      // Calculate total balance
      totalBalance = accounts.reduce((acc, current) => acc + current.balance, 0);
      
    } catch (err) {
      error = err.message || "Error al cargar las cuentas";
    } finally {
      loading = false;
    }
  });

  function formatCurrency(value) {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(value);
  }
</script>

<div class="space-y-6 animate-fade-in">
  
  {#if error}
    <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 text-red-400 text-sm">
      {error}
    </div>
  {/if}

  {#if loading}
    <!-- Skeleton loader for Total Balance -->
    <div class="bg-gradient-to-br from-dark-card to-dark-surface border border-dark-border rounded-3xl p-8 shadow-lg text-center animate-pulse">
      <div class="h-4 bg-dark-border rounded w-32 mx-auto mb-4"></div>
      <div class="h-10 bg-dark-border rounded w-48 mx-auto"></div>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
      {#each Array(4) as _}
        <div class="bg-dark-card border border-dark-border rounded-2xl p-6 h-32 animate-pulse">
          <div class="h-4 bg-dark-border rounded w-1/3 mb-4"></div>
          <div class="h-8 bg-dark-border rounded w-1/2"></div>
        </div>
      {/each}
    </div>
  {:else}
    <!-- Total Balance Hero -->
    <div class="bg-gradient-to-br from-dark-card to-dark-surface border border-dark-border rounded-3xl p-8 shadow-xl text-center relative overflow-hidden group">
      <div class="absolute inset-x-0 bottom-0 h-1/2 bg-gradient-to-t from-brand/5 to-transparent pointer-events-none"></div>
      <h2 class="text-sm font-medium text-slate-400 mb-3 uppercase tracking-widest">Patrimonio Total (Activos)</h2>
      <div class="text-5xl font-bold tracking-tight {totalBalance >= 0 ? 'text-white' : 'text-red-400'} drop-shadow-md">
        {formatCurrency(totalBalance)}
      </div>
    </div>

    <div class="flex items-center gap-2 mt-8 mb-4 px-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-brand" viewBox="0 0 20 20" fill="currentColor">
        <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
        <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
      </svg>
      <h3 class="text-lg font-semibold text-slate-200">Mis Cuentas</h3>
    </div>

    <!-- Accounts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#each accounts as account}
        <div class="bg-dark-card border border-dark-border rounded-2xl p-6 shadow hover:shadow-lg hover:border-dark-border/80 transition-all flex flex-col justify-between group relative overflow-hidden">
          
          <div class="flex justify-between items-start mb-4">
            <h4 class="text-base font-medium text-slate-300 group-hover:text-brand-light transition-colors line-clamp-1 pr-4">
              {account.name}
            </h4>
            
            <div class="p-2 bg-dark-surface rounded-lg text-slate-500 flex-shrink-0">
               <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
          
          <div>
            <div class="text-2xl font-bold {account.balance >= 0 ? 'text-white' : 'text-red-400'}">
              {new Intl.NumberFormat('es-ES', { style: 'currency', currency: account.currency_code || 'EUR' }).format(account.balance)}
            </div>
            
            <!-- Optional sparkline placeholder -> You could replace this div with a tiny history graph later -->
            <div class="mt-4 h-8 flex items-end opacity-30 gap-1" aria-hidden="true">
              <div class="w-full bg-emerald-500 rounded-t-sm h-full max-h-4"></div>
              <div class="w-full bg-emerald-500 rounded-t-sm h-full max-h-5"></div>
              <div class="w-full bg-emerald-500 rounded-t-sm h-full max-h-7"></div>
              <div class="w-full bg-emerald-500 rounded-t-sm h-full max-h-6"></div>
              <div class="w-full bg-emerald-500 rounded-t-sm h-full max-h-full"></div>
            </div>
          </div>
        </div>
      {/each}
      
      {#if accounts.length === 0}
         <div class="col-span-full p-8 text-center text-slate-500 flex flex-col items-center border border-dashed border-dark-border rounded-2xl">
           <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mb-3 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          No se detectaron cuentas de activo en Firefly III.
         </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .animate-fade-in {
    animation: fadeIn 0.4s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
