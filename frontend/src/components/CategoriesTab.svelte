<script>
  import { onMount } from 'svelte';
  import axios from 'axios';
  import Chart from './Chart.svelte';
  import EntityModal from './EntityModal.svelte';

  export let startDate;
  export let endDate;

  let categories = [];
  let loading = true;
  let error = null;
  let chartData = null;

  // Drilldown Modal
  let selectedCategory = null;

  // Re-fetch when dates change
  $: if (startDate && endDate) {
    fetchCategories();
  }

  async function fetchCategories() {
    loading = true;
    error = null;
    try {
      const url = `/api/categories?start=${startDate}&end=${endDate}`;
      const response = await axios.get(url);
      
      if (response.data && response.data.length > 0 && response.data[0].error) {
        throw new Error(response.data[0].error);
      }
      
      categories = response.data;
      
      if (categories.length > 0) {
        chartData = {
          labels: categories.map(c => c.name),
          datasets: [{
            label: 'Gasto por Categoría',
            data: categories.map(c => c.amount),
            backgroundColor: 'rgba(16, 185, 129, 0.8)', // Emerald
            borderRadius: 6,
            borderWidth: 0
          }]
        };
      } else {
        chartData = null;
      }
      
    } catch (err) {
      error = err.message || "Error al cargar las categorías";
    } finally {
      loading = false;
    }
  }

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
    <div class="bg-dark-card rounded-3xl p-6 h-[400px] animate-pulse"></div>
  {:else if categories.length === 0}
    <div class="bg-dark-card border border-dark-border rounded-3xl p-12 text-center text-slate-500 shadow-lg flex flex-col items-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-slate-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
      </svg>
      No hay gastos categorizados en este periodo.
    </div>
  {:else}
    <!-- Chart Section -->
    <section class="bg-dark-card border border-dark-border rounded-3xl p-4 md:p-6 shadow-lg">
      <div class="h-[300px] md:h-[400px] w-full">
        {#if chartData}
          <Chart data={chartData} type="bar" title="Gastos por Categoría" />
        {/if}
      </div>
    </section>

    <!-- List Section (Interactive) -->
    <section class="bg-dark-card border border-dark-border rounded-3xl overflow-hidden shadow-lg mt-6 mb-12">
      <div class="px-6 py-4 border-b border-dark-border/50">
        <h3 class="font-semibold text-white">Desglose Detallado</h3>
      </div>
      <div class="divide-y divide-dark-border/50">
        {#each categories as cat}
          <button 
            class="w-full p-4 flex items-center justify-between hover:bg-dark-surface/50 transition-colors text-left group"
            on:click={() => selectedCategory = cat.name}
          >
            <div class="flex items-center gap-3">
              <div class="p-2 bg-dark-surface border border-dark-border rounded-lg text-slate-400 group-hover:text-brand-light group-hover:border-brand/30 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
              </div>
              <span class="font-medium text-slate-200 group-hover:text-brand-light transition-colors">{cat.name}</span>
            </div>
            <div class="text-right flex items-center gap-3">
              <span class="font-bold text-red-400">-{formatCurrency(cat.amount)}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-500 group-hover:text-brand-light opacity-50 group-hover:opacity-100 transition-all" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>
        {/each}
      </div>
    </section>
  {/if}
</div>

{#if selectedCategory}
  <EntityModal 
    filterType="category" 
    filterValue={selectedCategory} 
    on:close={() => selectedCategory = null} 
  />
{/if}

<style>
  .animate-fade-in {
    animation: fadeIn 0.4s ease-out;
  }
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
