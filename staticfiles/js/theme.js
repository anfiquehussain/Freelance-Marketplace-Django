document.addEventListener('DOMContentLoaded', function () {
    console.log('DOMContentLoaded event fired!');
    const root = document.documentElement;
    const toggleButton = document.querySelector('.theme-toggle-button');

    // Function to set the theme based on user's preference or system preference
    const setTheme = (theme) => {
        root.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Update toggle button text based on the new theme
        updateToggleButtonText();
    };

    // Function to get the theme from localStorage or system preference
    const getSavedTheme = () => {
        return localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    };

    const updateToggleButtonText = () => {
        const currentTheme = root.getAttribute('data-theme');
        const buttonText = currentTheme === 'light' ? ' <i class="fa-solid fa-moon"></i>' : '<i class="fa-solid fa-sun"></i>';
    
        toggleButton.innerHTML = buttonText;
    
        // Add and remove the 'active' class for the fade-in/fade-out effect
        const icons = toggleButton.querySelectorAll('.fa-moon, .fa-sun');
        icons.forEach(icon => icon.classList.remove('active'));
    
        setTimeout(() => {
            icons.forEach(icon => icon.classList.add('active'));
        }, 0);
    };
    

    // Initial theme setting
    setTheme(getSavedTheme());

    // Event listener for changes in system theme
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        setTheme(getSavedTheme());
    });

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const currentTheme = root.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            setTheme(newTheme);
        });
    }
});
