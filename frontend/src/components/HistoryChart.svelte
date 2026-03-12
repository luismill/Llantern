<script>
  import { onMount, onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  // Data expects an array of objects: { label: '2026-03', income: 1000, expenses: 800, balance: 200 }
  export let data = [];
  export let title = 'Evolución Histórica (Últimos 6 meses)';

  let canvas;
  let chart;

  onMount(() => {
    initChart();
  });

  $: if (chart && data && data.length > 0) {
    updateChartData();
  } else if (!chart && data && data.length > 0 && canvas) {
    initChart();
  }

  function initChart() {
    if (!canvas) return;
    
    chart = new Chart(canvas, {
      type: 'line',
      data: getChartData(),
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        plugins: {
          legend: {
            display: true,
            labels: {
              color: '#cbd5e1',
              font: { family: "'Outfit', sans-serif" }
            }
          },
          title: {
            display: true,
            text: title,
            color: '#cbd5e1',
            font: {
              family: "'Outfit', sans-serif",
              size: 16,
              weight: 500
            }
          },
          tooltip: {
            backgroundColor: '#1e1e1e',
            titleColor: '#f8fafc',
            bodyColor: '#cbd5e1',
            borderColor: '#333333',
            borderWidth: 1,
            padding: 10,
            callbacks: {
               label: function(context) {
                let label = context.dataset.label || '';
                if (label) {
                  label += ': ';
                }
                if (context.parsed.y !== null) {
                  label += new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                }
                return label;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            grid: {
              color: '#333333',
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: { family: "'Outfit', sans-serif" },
              callback: function(value) {
                return value + ' €';
              }
            }
          },
          x: {
            grid: {
              display: false,
              drawBorder: false,
            },
            ticks: {
              color: '#94a3b8',
              font: { family: "'Outfit', sans-serif" }
            }
          }
        },
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        }
      }
    });
  }

  function getChartData() {
    return {
      labels: data.map(d => d.label),
      datasets: [
        {
          label: 'Ingresos',
          data: data.map(d => d.income),
          borderColor: '#10b981', // brand green
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          fill: true
        },
        {
          label: 'Gastos',
          data: data.map(d => d.expenses),
          borderColor: '#ef4444', // red
          backgroundColor: 'transparent',
          borderWidth: 2,
          tension: 0.4,
          fill: false
        }
      ]
    };
  }

  function updateChartData() {
    chart.data = getChartData();
    chart.update();
  }

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<div class="relative w-full h-full min-h-[300px]">
  {#if data.length === 0}
    <div class="absolute inset-0 flex items-center justify-center text-slate-500">
      Cargando historial...
    </div>
  {/if}
  <canvas bind:this={canvas}></canvas>
</div>
