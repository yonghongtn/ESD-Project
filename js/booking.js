/* This is for booking */
const app = Vue.createApp({
    data() {
        return {
        }
    },
    methods:{
        redirect(){
            window.location.href = "upload_qr.html"
        }
    }
})
app.mount('#app')