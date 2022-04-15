const lightIcon = document.querySelector('.light');
const darkIcon = document.querySelector('.dark');
const userTheme = localStorage.getItem('theme');

const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;

const iconToggle = () => {
  darkIcon.classList.toggle('hidden');
  lightIcon.classList.toggle('hidden');
};

const themeCheck = () => {
  if (userTheme === 'dark' || (!userTheme && systemTheme)) {
    document.documentElement.classList.add('dark');
    darkIcon.classList.add('hidden');
    return;
  }
  lightIcon.classList.add('hidden');
};