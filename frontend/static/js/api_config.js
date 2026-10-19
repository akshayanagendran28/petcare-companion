/**
 * Pet Care Companion - Frontend API & Cloud Gateway Configuration
 * Auto-detects whether running on Vercel Edge, Render, or Localhost,
 * and routes API requests to the appropriate backend service.
 */
(function() {
  const metaTag = document.querySelector('meta[name="petcare-backend-url"]');
  const storedUrl = localStorage.getItem('petcare_backend_url');
  
  // Render default backend or custom URL
  const defaultBackend = metaTag ? metaTag.content : (storedUrl || window.location.origin);

  window.PETCARE_CONFIG = {
    backendUrl: defaultBackend,
    isVercel: window.location.hostname.endsWith('vercel.app'),
    isRender: window.location.hostname.endsWith('onrender.com'),
    isLocal: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
    getApiUrl: function(path) {
      if (!path.startsWith('/')) path = '/' + path;
      // In same-origin or reverse proxy mode, relative path is always preferred
      if (this.isLocal || !storedUrl) {
        return path;
      }
      return `${this.backendUrl.replace(/\/$/, '')}${path}`;
    }
  };

  // Log active cloud runtime
  const envName = window.PETCARE_CONFIG.isVercel ? 'Vercel (Frontend)' : 
                 (window.PETCARE_CONFIG.isRender ? 'Render (Backend & DB)' : 'Local Development');
  console.log(`🐾 Pet Care Companion initialized in [${envName}] mode.`);
})();
