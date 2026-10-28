import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)


app.config.globalProperties.$formatDate = (dateString) => {
    if (!dateString) return '';

    const value = String(dateString).trim();
    let year, month, day;

    // Format: YYYY-MM-DD
    let match = value.match(/^(\d{4})-(\d{2})-(\d{2})$/);

    if (match) {
        [, year, month, day] = match;
    } else {
        // Formats: DD-MM-YYYY or DD/MM/YYYY
        match = value.match(/^(\d{2})[-/](\d{2})[-/](\d{4})$/);

        if (match) {
            [, day, month, year] = match;
        } else {
            // Format: DD Mon YYYY, e.g. 27 Oct 2026
            match = value.match(
                /^(\d{1,2})\s+([A-Za-z]{3,})\s+(\d{4})$/
            );

            if (match) {
                day = match[1];
                year = match[3];

                const monthNames = [
                    'jan', 'feb', 'mar', 'apr',
                    'may', 'jun', 'jul', 'aug',
                    'sep', 'oct', 'nov', 'dec'
                ];

                month = monthNames.indexOf(
                    match[2].slice(0, 3).toLowerCase()
                ) + 1;

                if (month === 0) return value;
            } else {
                // Handle valid datetime strings separately.
                const parsed = new Date(value);

                if (Number.isNaN(parsed.getTime())) {
                    console.warn('Invalid date received:', value);
                    return value;
                }

                return new Intl.DateTimeFormat('en-GB', {
                    day: '2-digit',
                    month: 'short',
                    year: 'numeric'
                }).format(parsed);
            }
        }
    }

    // Validate the date before formatting it.
    year = Number(year);
    month = Number(month);
    day = Number(day);

    const date = new Date(year, month - 1, day);

    if (
        date.getFullYear() !== year ||
        date.getMonth() !== month - 1 ||
        date.getDate() !== day
    ) {
        console.warn('Invalid date received:', value);
        return value;
    }

    return new Intl.DateTimeFormat('en-GB', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    }).format(date);
};


app.mount('#app')
