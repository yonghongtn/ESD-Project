const app = Vue.createApp({
    data() {
        return {
            plateNo: sessionStorage.getItem("vehicle_to_view_plateno"),
            brand: sessionStorage.getItem("vehicle_to_view_brand"),
            model: sessionStorage.getItem("vehicle_to_view_model"),
            location: sessionStorage.getItem("vehicle_to_view_location"),
            price: sessionStorage.getItem("vehicle_to_view_price"),
            imgsrc: "img/" + sessionStorage.getItem("vehicle_to_view_brand") + " " + sessionStorage.getItem("vehicle_to_view_model") + ".png",
            PriceID: sessionStorage.getItem("vehicle_to_view_priceid"),
            hours_booked: 1
        }
    },
    methods:{
        goBack(){
            window.location.href = "index.html"
        },
        async bookVehicle(){
            /* Call stripe flask app */
            //console.log({"price": this.PriceID, "quantity": this.hours_booked})
            var fetch_url = "http://localhost:5006/create-checkout-session" + "/" + this.PriceID + "/" + this.hours_booked
            const response = await fetch(fetch_url)
            const result = await response.json();
            console.log(result.url)
            //store session id in session storage
            sessionStorage.setItem("payment_session_id", result.sessionId)
            sessionStorage.setItem("hours_booked", this.hours_booked)
            window.location.replace(result.url);
        }
    },
    computed:{
        getImgSrc(){
            return "img/" + this.brand + " " + this.model + ".png"
        }
    }
})

app.mount('#app')