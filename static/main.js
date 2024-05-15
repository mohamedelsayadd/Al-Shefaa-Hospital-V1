/*==================== DARK LIGHT THEME ====================*/ 
const themeButton = document.getElementById('theme-button');
const darkTheme = 'dark-theme';
const iconTheme = 'bx-sun';
const header = document.getElementById('header');

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme');
const selectedIcon = localStorage.getItem('selected-icon');

// Function to set header color based on theme
const setHeaderColor = () => {
    if (getCurrentTheme() === 'dark') {
        header.style.backgroundImage = 'linear-gradient(346deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 22%,rgba(143,136,136, 0.04) 22%, rgba(143,136,136, 0.04) 69%,rgba(143,136,136, 0.04) 69%, rgba(143,136,136, 0.04) 100%),linear-gradient(31deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 42%,rgba(143,136,136, 0.04) 42%, rgba(143,136,136, 0.04) 85%,rgba(143,136,136, 0.04) 85%, rgba(143,136,136, 0.04) 100%),linear-gradient(55deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 13%,rgba(143,136,136, 0.04) 13%, rgba(143,136,136, 0.04) 72%,rgba(143,136,136, 0.04) 72%, rgba(143,136,136, 0.04) 100%),linear-gradient(90deg, rgb(11,11,11),rgb(11,11,11))';
        header.style.color = 'white'; // You may need to adjust text color accordingly
    } else {
        header.style.backgroundImage = 'linear-gradient(346deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 22%,rgba(143,136,136, 0.04) 22%, rgba(143,136,136, 0.04) 69%,rgba(143,136,136, 0.04) 69%, rgba(143,136,136, 0.04) 100%),linear-gradient(31deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 42%,rgba(143,136,136, 0.04) 42%, rgba(143,136,136, 0.04) 85%,rgba(143,136,136, 0.04) 85%, rgba(143,136,136, 0.04) 100%),linear-gradient(55deg, rgba(242,242,242, 0.04) 0%, rgba(242,242,242, 0.04) 13%,rgba(143,136,136, 0.04) 13%, rgba(143,136,136, 0.04) 72%,rgba(143,136,136, 0.04) 72%, rgba(143,136,136, 0.04) 100%),linear-gradient(90deg, rgb(250,250,250),rgb(250,250,250))';
        header.style.color = 'black'; // You may need to adjust text color accordingly
    }
};

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light';

// We validate if the user previously chose a topic
if (selectedTheme) {
    // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme);
    themeButton.classList[selectedIcon === 'bx-moon' ? 'add' : 'remove'](iconTheme);
    setHeaderColor();
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme);
    themeButton.classList.toggle(iconTheme);
    // Set header color based on theme
    setHeaderColor();
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme());
    localStorage.setItem('selected-icon', getCurrentIcon());
});
