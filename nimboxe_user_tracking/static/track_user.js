async function trackUser(path = window.location.pathname) {
  try {
    // 1️⃣ Obtener datos geográficos del usuario
    const res = await fetch('https://ipapi.co/json/');
    if (!res.ok) throw new Error('Error al obtener datos de IP');
    const data = await res.json();

    // 2️⃣ Construir objeto para el backend
    const visitData = {
      ip: data.ip,
      city: data.city,
      region: data.region,
      postal: data.postal,
      country: data.country_name,  // backend espera 'country'
      timezone: data.timezone,
      org: data.org,
      path: path,
      user_agent: navigator.userAgent
    };

    // 3️⃣ Enviar datos al backend
    const backendRes = await fetch('http://localhost:8000/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(visitData)
    });

    if (!backendRes.ok) throw new Error('Error al enviar datos al backend');

    console.log('Usuario trackeado correctamente', visitData);
  } catch (err) {
    console.error('Error en tracking:', err);
  }
}

// Llamar al cargar la página
trackUser();
