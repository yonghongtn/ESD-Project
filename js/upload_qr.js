/* This is the Vue app for uploading QR code */
const app = Vue.createApp({
    data() {
        return {
            image: null,
        }
    },
    methods:{
        redirect(){
            window.location.href = "booking.html"
        }
    }
})

app.mount('#app')