document.getElementById('language').addEventListener('change', function() {
    const selectedLanguage = this.value;
    
    // Get the current URL path (e.g., /repository-name/index.html)
    let currentPath = window.location.pathname;
    
    if (selectedLanguage === 'en') {
        // If we are on the default page, replace it with the English file
        if (currentPath.endsWith('/') || currentPath.endsWith('index.html')) {
            window.location.href = 'index-en.html';
        }
    } else if (selectedLanguage === 'vi') {
        if (currentPath.endsWith('index-en.html')) {
            window.location.href = 'index.html';
        }
    }
});