document.addEventListener('DOMContentLoaded', () => {
  const button = document.getElementById('clean-btn');

  button.addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        chrome.scripting.executeScript({
          target: { tabId: tabs[0].id },
          func: cleanPage
        });
      }
    });
  });
});

function cleanPage() {
  // === SCHRITT 1: Die "Schwarze Liste" der Selektoren ===
  // Wir nutzen CSS-Selektoren. 
  // [href*="wort"] bedeutet: Jedes Element, dessen Link "wort" enthält.
  const selectorsToRemove = [
    // Standard Multimedia
    'img', 'iframe', 'video', 'canvas', 'svg', 'embed', 'object',
    
    // Werbe-Container (Tags)
    'ins', 'aside', 
    
    // Werbe-URLs erkennen (Das ist neu und wichtig für Ihren Fall!)
    '[href*="googleads"]',       // Links zu Google Ads
    '[href*="doubleclick"]',     // Doubleclick Tracker
    '[href*="flashtalking"]',    // Flashtalking (aus Ihrem Beispiel)
    '[src*="flashtalking"]',     // Bilder von Flashtalking
    '[href*="adsystem"]',
    '[href*="adserver"]',
    
    // Werbe-Klassen und IDs (häufige Begriffe)
    '[id*="banner"]', '[class*="banner"]',
    '[id*="adv"]',    '[class*="adv"]',
    '[class*="sponsored"]',
    '[aria-label="Anzeige"]',
    '[aria-label="Ads"]'
  ];

  const selectorString = selectorsToRemove.join(',');

  // === SCHRITT 2: Löschen statt nur Verstecken ===
  const elements = document.querySelectorAll(selectorString);
  elements.forEach(el => {
    // Wir löschen das Element komplett aus dem DOM
    el.remove();
  });

  // === SCHRITT 3: Visuelle Ruhe (Reiner Text) ===
  // Alles auf Standard setzen
  document.body.style.background = '#fdf6e3'; // Beige Farbe erzwingen
  document.body.style.color = '#333';
  document.body.style.fontFamily = 'Georgia, serif';
  document.body.style.lineHeight = '1.6';
  
  // Ränder aufräumen (falls durch gelöschte Werbung Lücken entstehen)
  document.body.style.margin = '0 auto';
  document.body.style.maxWidth = '800px'; // Textbreite begrenzen für Lesbarkeit
  document.body.style.padding = '40px';
}