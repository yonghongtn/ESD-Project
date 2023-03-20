/* This is for trip ended */
const app = Vue.createApp({
    data() {
        return {
        }
    },
    methods:{
        redirect(){
            window.location.href = "index.html"
        }
    }
})
app.mount('#app')