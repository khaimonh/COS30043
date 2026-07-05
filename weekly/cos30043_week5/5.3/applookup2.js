var units = [
    {
        code: 'ICT10001',
        desc: 'Problem Solving with ICT',
        cp: '12.5',
        type: 'Core',
    },
    { code: 'COS10005', desc: 'Web Development', cp: '12.5', type: 'Core' },
    {
        code: 'INF10003',
        desc: 'Introduction to Business Information Systems',
        cp: '12.5',
        type: 'Core',
    },
    {
        code: 'INF10002',
        desc: 'Database Analysis and Design',
        cp: '12.5',
        type: 'Core',
    },
    {
        code: 'COS10009',
        desc: 'Introduction to Programming',
        cp: '12.5',
        type: 'Core',
    },
    {
        code: 'INF30029',
        desc: 'Information Technology Project Management',
        cp: '12.5',
        type: 'Core',
    },
    {
        code: 'ICT30005',
        desc: 'Professional Issues in Information Technology',
        cp: '12.5',
        type: 'Core',
    },
    {
        code: 'ICT30001',
        desc: 'Information Technology Project',
        cp: '12.5',
        type: 'Core',
    },
]

const Unit = {
    data() {
        return { units }
    },
    template: `
        <div v-if="filteredUnit" style="margin-top: 20px; border-top: 1px solid #ccc; padding-top: 10px;">
            <h3>Unit Code: {{ filteredUnit.code }}</h3>
            <ul>
                <li>{{ filteredUnit.code }}</li>
                <li>{{ filteredUnit.desc }}</li>
                <li>{{ filteredUnit.cp }}</li>
                <li>{{ filteredUnit.type }}</li>
            </ul>
        </div>
    `,
    computed: {
        filteredUnit() {
            const unitCode = this.$route.params.id
            return this.units.find((u) => u.code === unitCode)
        },
    },
}

const router = VueRouter.createRouter({
    history: VueRouter.createWebHashHistory(),
    routes: [
        { path: '/unit/:id', component: Unit },
    ],
})

const app = Vue.createApp({})

app.component('app-lookup2', {
    data: function () {
        return { units }
    },
    template: `
        <div>
            <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
                <thead>
                    <tr align="left">
                        <th>Code</th>
                        <th>Description</th>
                        <th>More Info</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="unit in units" :key="unit.code">
                        <td>{{ unit.code }}</td>
                        <td>{{ unit.desc }}</td>
                        <td>
                            <router-link :to="'/unit/' + unit.code">show details</router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <router-view></router-view>
        </div>
    `,
})

app.use(router)
app.mount('#app')
