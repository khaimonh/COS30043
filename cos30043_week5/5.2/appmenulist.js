const app = Vue.createApp({})

app.component('mymenu', {
    props: ['menu'], // Accept the array string from the parent
    template: `
        <ul>
            <li v-for="item in menu" :key="item">
                {{ item }}
            </li>
        </ul>
    `,
})

app.mount('#app')
