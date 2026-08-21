// Auto-detect system dark mode (only if no saved theme)
(function(){
  if(!localStorage.getItem('wutz-theme')&&window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches){
    document.documentElement.setAttribute('data-theme','darktech');
    document.querySelectorAll('.theme-btn').forEach(function(b){
      b.classList.toggle('active',b.dataset.theme==='darktech');
    });
  }
})();
