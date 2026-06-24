const app = Vue.createApp({})

app.component('app-mypost', {
    data: function () {
        return {
            statPosts: [],
            strStatus: '',
        }
    },

    template: `
        <div>
            <label for="statusBox">Status: </label>
            <input id="statusBox" type="text" v-model="strStatus">
            <button @click="add(strStatus)">Post</button>
            
            <div style="margin-top: 20px;">
                <div v-for="(post, index) in statPosts" :key="index" style="margin-bottom: 8px;">
                    <span>{{ post }}</span>
                    <button @click="remove(index)" style="margin-left: 5px;">Del</button>
                </div>
            </div>
        </div>
    `,
    methods: {
        add: function (status) {
            if (status.trim() !== '') {
                this.statPosts.unshift(status)
                this.strStatus = ''
            }
        },
        remove: function (index) {
            this.statPosts.splice(index, 1)
        },
    },
})

app.mount('#app')
