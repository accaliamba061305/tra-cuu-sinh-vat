document.getElementById('language').addEventListener('change', function() {
    const selectedLanguage = this.value;
    
    if (selectedLanguage === 'en') {
        window.location.href = 'index-en.html'; // Go to English page
    } else if (selectedLanguage === 'vi') {
        window.location.href = 'index.html';    // Go to Vietnamese page
    }
});