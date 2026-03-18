export function getCategoryIcon(categoryName) {
  if (!categoryName) return getDefaultIcon();
  
  const name = categoryName.toLowerCase();
  
  // Supermercado / Comida
  if (name.includes('super') || name.includes('compra') || name.includes('comida') || name.includes('aliment') || name.includes('mercado')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>`;
  }
  // Transporte / Coche / Gasolina
  if (name.includes('transporte') || name.includes('coche') || name.includes('gasolina') || name.includes('bus') || name.includes('tren') || name.includes('parking') || name.includes('vehi') || name.includes('viaje')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>`;
  }
  // Restaurantes / Ocio / Bares / Salidas
  if (name.includes('restaurante') || name.includes('bar') || name.includes('ocio') || name.includes('salida') || name.includes('cine') || name.includes('cena')) {
    if (name.includes('bar')) {
      return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-1.605.42-3.113 1.157-4.418" /></svg>`; // Wait... let me find a better beer SVG later or just use emoji SVG, no, wait...
    }
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 15.546c-.523 0-1.046.151-1.5.454a2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.704 2.704 0 00-3 0 2.704 2.704 0 01-3 0 2.701 2.701 0 00-1.5-.454M9 6v2m3-2v2m3-2v2M9 3h.01M12 3h.01M15 3h.01M21 21v-7a2 2 0 00-2-2H5a2 2 0 00-2 2v7h18zm-3-9v-2a2 2 0 00-2-2H8a2 2 0 00-2 2v2h12z" /></svg>`;
  }
  // Alojamiento / Hotel
  if (name.includes('alojamiento') || name.includes('hotel')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1v1H9V7zm5 0h1v1h-1V7zm-5 4h1v1H9v-1zm5 0h1v1h-1v-1zm-3 4H9m5 0h-2" /></svg>`;
  }
  // Deporte / Gimnasio
  if (name.includes('deporte') || name.includes('sport')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>`; // Using lightning bolt as sport for now, will replace with proper later
  }
  // Casa / Hogar / Alquiler / Facturas
  if (name.includes('casa') || name.includes('hogar') || name.includes('alquiler') || name.includes('luz') || name.includes('agua') || name.includes('internet') || name.includes('factura') || name.includes('hipoteca')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>`;
  }
  // Salud / Farmacia
  if (name.includes('salud') || name.includes('farmacia') || name.includes('médico') || name.includes('medico') || name.includes('dentista') || name.includes('hospital')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>`;
  }
  // Ropa / Compras misceláneas / Regalos
  if (name.includes('ropa') || name.includes('regalo') || name.includes('shopping') || name.includes('moda') || name.includes('personal')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" /></svg>`;
  }
  // Sueldo / Ingresos / Nómina
  if (name.includes('sueldo') || name.includes('ingreso') || name.includes('nomina') || name.includes('nómina') || name.includes('salario') || name.includes('interés')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`;
  }
  // Seguros
  if (name.includes('seguro')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>`;
  }
  // Mascotas
  if (name.includes('mascota') || name.includes('perro') || name.includes('gato') || name.includes('vet')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`; // Face
  }
  // Suscripciones
  if (name.includes('suscrip') || name.includes('netflix') || name.includes('spotify') || name.includes('gimnasio')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" /></svg>`; // Archive box / Subscription
  }
  // Tarjetas / Bancos / Comisiones
  if (name.includes('tarjeta') || name.includes('comision') || name.includes('comisión') || name.includes('banco') || name.includes('prestamo')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" /></svg>`; // Credit card
  }

  return getDefaultIcon();
}

function getDefaultIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>`;
}

export function getAccountLogo(accountName) {
  if (!accountName) return getDefaultAccountIcon();
  
  const name = accountName.toLowerCase();
  
  // Revolut
  if (name.includes('revolut')) {
    return `<svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor"><path d="M16.5 0h-9L4.8 6.4h9L16.5 0zm2.25 15.65h-6.85v3.45H8v4.9h2.35v-4.9h3.45L18.75 24h3.1l-6-5.85c2.35-.6 4-2.75 4-5.3 0-3.3-2.7-5.95-6-5.95h-5.15v2.3h5.15c2.05 0 3.7 1.6 3.7 3.65 0 2.05-1.65 3.7-3.7 3.7z"/></svg>`;
  }
  
  // BBVA
  if (name.includes('bbva')) {
    // Basic text based SVG tailored for BBVA styling
    return `<svg viewBox="0 0 64 24" class="h-6" style="width: auto;" fill="currentColor"><text x="0" y="19" font-family="'Open Sans', sans-serif" font-weight="800" font-size="22" letter-spacing="-1.5">BBVA</text></svg>`;
  }
  
  // Laboral Kutxa (LK box representation or text)
  if (name.includes('laboral') || name.includes('kutxa')) {
    return `<svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor"><rect width="24" height="24" rx="4" fill="#E8006E"/><text x="12" y="17" dominant-baseline="middle" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-weight="900" font-size="14">lk</text></svg>`;
  }
  
  // Efectivo
  if (name.includes('efectivo') || name.includes('cash') || name.includes('metálico')) {
    return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" /></svg>`;
  }

  return getDefaultAccountIcon();
}

function getDefaultAccountIcon() {
  return `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" /></svg>`;
}
