/* This is for trip ended */
const app = Vue.createApp({
    data() {
        return {
            message:null
        }
    },
    methods:{
        redirect(){
            window.location.href = "index.html"
        }
    },
    created(){
        if (sessionStorage.getItem("message")!=null){
            this.message = sessionStorage.getItem("message")
        }
    }
})
app.mount('#app')