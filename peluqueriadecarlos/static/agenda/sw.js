const CACHE_NAME = "citas-barberia-v1";
const urlsToCache = [
    "/",
    "/static/agenda/css/estilos.css",
    "/static/agenda/manifest.json",
    "/static/agenda/icons/carlosimagen.ico",
    "/static/agenda/icons/carlosimagen.ico",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css",
    "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap"
];
// Instalación del Service Worker
self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
            .catch(err => console.error("❌ Error al agregar archivos al caché:", err))
    );
});

// Activación: Borra versiones antiguas del caché
self.addEventListener("activate", event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => cacheName !== CACHE_NAME)
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Intercepta las peticiones de red y usa el caché si está disponible
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request).catch(() => {
                console.warn("❌ No se pudo recuperar el recurso:", event.request.url);
            });
        })
    );
});
