<script>
  import DashboardTab from './components/DashboardTab.svelte';
  import TransactionsTab from './components/TransactionsTab.svelte';
  import AccountsTab from './components/AccountsTab.svelte';

  let currentTab = 'dashboard'; // 'dashboard', 'transactions', 'accounts'

  function switchTab(tab) {
    currentTab = tab;
  }
</script>

<main class="min-h-screen bg-dark-bg text-slate-200 font-sans selection:bg-brand selection:text-white pb-24">
  <header class="sticky top-0 z-50 bg-dark-surface/80 backdrop-blur-md border-b border-dark-border px-6 py-4 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-full bg-brand flex items-center justify-center shadow-neon">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 2a4 4 0 00-4 4v1H5a1 1 0 00-.994.89l-1 9A1 1 0 004 18h12a1 1 0 00.994-1.11l-1-9A1 1 0 0015 7h-1V6a4 4 0 00-4-4zm2 5V6a2 2 0 10-4 0v1h4zm-6 3a1 1 0 112 0 1 1 0 01-2 0zm7-1a1 1 0 100 2 1 1 0 000-2z" clip-rule="evenodd" />
        </svg>
      </div>
      <h1 class="text-xl font-bold tracking-tight text-white">Llantern</h1>
    </div>
  </header>

  <div class="max-w-4xl mx-auto px-4 py-8">
    {#if currentTab === 'dashboard'}
      <DashboardTab />
    {:else if currentTab === 'transactions'}
      <TransactionsTab />
    {:else if currentTab === 'accounts'}
      <AccountsTab />
    {/if}
  </div>

  <!-- Bottom Navigation Tab Bar -->
  <div class="fixed bottom-0 left-0 right-0 z-50 bg-dark-surface/90 backdrop-blur-md border-t border-dark-border px-6 py-3 pb-safe">
    <div class="max-w-md mx-auto flex justify-between items-center">
      
      <!-- Dashboard Tab -->
      <button 
        class="flex flex-col items-center gap-1 transition-colors {currentTab === 'dashboard' ? 'text-brand' : 'text-slate-500 hover:text-slate-300'}"
        on:click={() => switchTab('dashboard')}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width={currentTab === 'dashboard' ? "2.5" : "2"} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
        </svg>
        <span class="text-[10px] font-medium uppercase tracking-wider">Resumen</span>
      </button>

      <!-- Transactions Tab -->
      <button 
        class="flex flex-col items-center gap-1 transition-colors {currentTab === 'transactions' ? 'text-brand' : 'text-slate-500 hover:text-slate-300'}"
        on:click={() => switchTab('transactions')}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width={currentTab === 'transactions' ? "2.5" : "2"} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
        <span class="text-[10px] font-medium uppercase tracking-wider">Movimientos</span>
      </button>

      <!-- Accounts Tab -->
      <button 
        class="flex flex-col items-center gap-1 transition-colors {currentTab === 'accounts' ? 'text-brand' : 'text-slate-500 hover:text-slate-300'}"
        on:click={() => switchTab('accounts')}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width={currentTab === 'accounts' ? "2.5" : "2"} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
        </svg>
        <span class="text-[10px] font-medium uppercase tracking-wider">Cuentas</span>
      </button>

    </div>
  </div>
</main>
