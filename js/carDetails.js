const app = Vue.createApp({
    data() {
        return {
            plateNo: sessionStorage.getItem("vehicle_to_view_plateno"),
            brand: sessionStorage.getItem("vehicle_to_view_brand"),
            model: sessionStorage.getItem("vehicle_to_view_model"),
            location: sessionStorage.getItem("vehicle_to_view_location"),
            price: sessionStorage.getItem("vehicle_to_view_price"),
            imgsrc: "img/" + sessionStorage.getItem("vehicle_to_view_brand") + " " + sessionStorage.getItem("vehicle_to_view_model") + ".png",
            hours_booked: 1
        }
    },
    methods:{
        goBack(){
            window.location.href = "index.html"
        },
        bookVehicle(){
            /* Store all vehicle attributes in session storage, then redirect to booking page */
            sessionStorage.setItem("vehicle_to_book_plateno", this.plateNo)
            sessionStorage.setItem("vehicle_to_book_brand", this.brand)
            sessionStorage.setItem("vehicle_to_book_model", this.model)
            sessionStorage.setItem("vehicle_to_book_price", this.price)
            sessionStorage.setItem("vehicle_to_book_hours", this.hours_booked)
            sessionStorage.setItem("status", "Booked")
            window.location.href = "booking.html"
        }
    },
    computed:{
        getImgSrc(){
            return "img/" + this.brand + " " + this.model + ".png"
        }
    }
})

app.mount('#app')