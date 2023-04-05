/* This is for booking */
const app = Vue.createApp({
    data() {
        return {
            // This is for the booking page
            plateNo: null,
            brand: null,
            model: null,
            hours_booked: null,
            start_time: null,
            img_url: null,
            location: null,
            error_message: null,
            lat: null,
            long: null,
            
        }
    },
    methods:{
        error(){
            this.error_message = "Please enable Geolocation"
        },
        success(position){
            this.lat = position.coords.latitude
            this.long = position.coords.longitude
            this.error_message = null
        },
        redirect(){
            window.location.href = "upload_qr.html"
        },
        async endtrip(){
            // check if geolocation is enabled
            if (!"geolocation" in navigator) {
                console.log("geolocation is not available")
                this.error_message = "Geolocation is not available"
            }
            else{
                navigator.geolocation.getCurrentPosition(this.success, this.error)
                //delay by 1 second
                await new Promise(r => setTimeout(r, 1000));
                if (this.lat != null){
                    //call parking handler microservice
                    var content_body = {
                        "driver_id" : sessionStorage.getItem("driverid"),
                        "rentalid": sessionStorage.getItem("rental_id"),
                        "coordinates":{
                            "lat": this.lat,
                            "lng": this.long
                        }
                    }
                    console.log(content_body)
                    var parking_response = await fetch("http://127.0.0.1:5100/parking_handler",
                    {
                        method: 'POST',
                        body: JSON.stringify(content_body),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                    var parking_result = await parking_response.json()
                    console.log(parking_result)
                    if (parking_result.code == 200){
                        //clear session storage
                        sessionStorage.clear()
                        //redirect to trip ended page
                        window.location.href = "trip_ended.html"
                    }
                    else{
                        this.error_message = parking_result.message
                    }
                }
            }
        }
    },
    created(){
        if (sessionStorage.getItem("payment_intent_id")==null){
            $(async() => {           
                // Change serviceURL to your own
                var serviceURL = "http://localhost:5006/retrieve-session/"+sessionStorage.getItem("payment_session_id");
                try {
                    const response =
                     await fetch(
                       serviceURL, { method: 'GET' }
                    );
                    const result = await response.json();
                    console.log(result)
                    //not paid yet
                     if (result.payment_intent==null) {
                        window.location.href = "index.html"
                    }
                    // else continue on website and call book trip
                    else{
                        //store payment intent in session storage
                        sessionStorage.setItem("payment_intent_id", result.payment_intent)
                        //call book trip
                        var content_body = {
                            "DriverID": sessionStorage.getItem("driverid"),
                            "PlateNo": sessionStorage.getItem("vehicle_to_view_plateno"),
                            "BookingDuration": sessionStorage.getItem("hours_booked"),
                            "TotalFare": sessionStorage.getItem("vehicle_to_view_price")*sessionStorage.getItem("hours_booked"),
                            "StartLocation": sessionStorage.getItem("vehicle_to_view_location_id")
                        }
                        console.log(content_body)
                        const booking_response = await fetch("http://localhost:5200/place_booking",
                        
                        {
                            method: 'POST',
                            body: JSON.stringify(content_body),
                            headers: {
                                'Content-Type': 'application/json'
                            },
                        })
                        const booking_result = await booking_response.json();
                        console.log(booking_result.data.data)
                        //Substitute in the variables
                        this.plateNo= sessionStorage.getItem("vehicle_to_view_plateno")
                        this.brand= sessionStorage.getItem("vehicle_to_view_brand")
                        this.model= sessionStorage.getItem("vehicle_to_view_model")
                        this.hours_booked= sessionStorage.getItem("hours_booked")
                        this.start_time= booking_result.data.data.StartTime
                        this.img_url = "img/"+this.brand + " " + this.model + ".png"
                        this.location = sessionStorage.getItem("vehicle_to_view_location")
                        sessionStorage.setItem("rental_id", booking_result.data.data.RentalID)
                        sessionStorage.setItem("start_time", booking_result.data.data.StartTime)
                    }
                }
                catch (error) {
                    console.log(error);
                }
            })
        }
        //redirected from change booking
        else{
            this.plateNo= sessionStorage.getItem("vehicle_to_view_plateno")
            this.brand= sessionStorage.getItem("vehicle_to_view_brand")
            this.model= sessionStorage.getItem("vehicle_to_view_model")
            this.location = sessionStorage.getItem("vehicle_to_view_location")
            this.hours_booked= sessionStorage.getItem("hours_booked")
            this.start_time= sessionStorage.getItem("start_time")
            this.img_url = "img/"+this.brand + " " + this.model + ".png"
        }
        
    }
})
app.mount('#app')