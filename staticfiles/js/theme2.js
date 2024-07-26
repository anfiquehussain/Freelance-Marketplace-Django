document.addEventListener('DOMContentLoaded', function() {
    const root = document.documentElement;
    const toggleButton = document.querySelector('.theme-toggle-button');
    const themeSelector = document.getElementById('theme-selector');

    // Function to set the theme
    function setTheme(theme) {
        root.setAttribute('data-theme', theme);
        localStorage.setItem('selectedTheme', theme);
    }

    // Function to retrieve the saved theme from localStorage
    function getSavedTheme() {
        return localStorage.getItem('selectedTheme') || 'system';
    }

    // Function to set the theme based on user preference, system preference, or saved preference
    function setThemeBasedOnUserPreference() {
        const selectedTheme = themeSelector.value;

        if (selectedTheme === 'system') {
            const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
            setTheme(prefersDarkMode ? 'dark' : 'light');
        } else {
            setTheme(selectedTheme);
        }
    }

    // Set the theme based on user preference, system preference, or saved preference when the page loads
    setTheme(getSavedTheme());
    themeSelector.value = getSavedTheme();

    // Event listener for theme selector changes
    themeSelector.addEventListener('change', setThemeBasedOnUserPreference);

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const currentTheme = root.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            setTheme(newTheme);
            themeSelector.value = newTheme;
        });
    }
});
