// Service worker van de RTT Veldplanner: de app opent ook zonder internet (bijvoorbeeld in de hal).
// De pagina zelf: eerst het netwerk (altijd de nieuwste versie), anders de bewaarde kopie.
// Lettertypes: eerst de bewaarde kopie. Supabase (velden) gaat er niet doorheen.
const CACHE = 'rtt-veldplanner-v1';
const CORE = ['./', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const u = new URL(e.request.url);
  if (u.origin === location.origin) {
    const key = e.request.mode === 'navigate' ? './' : e.request;
    e.respondWith(fetch(e.request).then(r => {
      if (r.ok) { const c = r.clone(); caches.open(CACHE).then(ca => ca.put(key, c)); }
      return r;
    }).catch(() => caches.match(key, {ignoreSearch: true}).then(r => r || caches.match('./'))));
  } else if (u.hostname === 'fonts.googleapis.com' || u.hostname === 'fonts.gstatic.com') {
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      const c = res.clone(); caches.open(CACHE).then(ca => ca.put(e.request, c)); return res;
    })));
  }
});
