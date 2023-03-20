/* This is for fault reporting */
const app = Vue.createApp({
    data() {
        return {
            faultTypes: ["Choose fault type", "Car cannot open", "Engine cannot start", "Flat type"],
            faultTypeSelected: "Choose fault type",
            faultDescription: "",
        }
    },
    created(){
        
    },
    methods:{
        goBack(){
            window.location.href = "booking.html"
        }
    }
})

app.mount('#app')