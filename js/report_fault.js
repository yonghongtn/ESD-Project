/* This is for fault reporting */
const app = Vue.createApp({
    data() {
        return {
            faultDescription: "",
            chosen_remedy: "Replace car with nearest available car",
            remedies: ["Replace car with nearest available car", "Refund"],
            submission_error : false,
            submission_error_message : "",
            lat: null,
            long: null,
            outcome:""
            
        }
    },
    created(){
        
    },
    methods:{
        goBack(){
            window.location.href = "booking.html"
        },
        error(){
            this.submission_error = true,
            this.submission_error_message = "Please enable Geolocation"
        },
        success(position){
            this.lat = position.coords.latitude
            this.long = position.coords.longitude
            this.submission_error = false,
            this.submission_error_message = null
        },
        async process_report(){
            if (this.submission_error == false){
                submit_to_manage_issue = {
                    "Report":{
                        "DriverID": sessionStorage.getItem("driverid"),
                        "RentalID": sessionStorage.getItem("rental_id"),
                        "PlateNo": sessionStorage.getItem("vehicle_to_view_plateno"),
                        "Outcome": this.chosen_remedy,
                        "Content": this.faultDescription
                    },
                    "Current Location": {'lat': this.lat, 'lng': this.long},
                    "PaymentID": sessionStorage.getItem("payment_intent_id"),
                    "PhoneNo": sessionStorage.getItem("mobile_number")
                
                }
                console.log(submit_to_manage_issue)
    
                const report_response = await fetch("http://localhost:5300/manage_issue",
                        
                    {
                            method: 'POST',
                            body: JSON.stringify(submit_to_manage_issue),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                    })
                const report_result = await report_response.json()
                console.log(report_result)
                
                //Replacement successful
                if (report_result.code != 200){
                    this.submission_error_message = report_result.message
                }
                else if (report_result.message == "Successfully processed replacement"){
                    // Display outcome on screen
                    this.outcome = "Successfully processed replacement, please go back to booking page to view new car details"
                    sessionStorage.setItem("vehicle_to_view_plateno", report_result.booking.data.PlateNo)
                    sessionStorage.setItem("vehicle_to_view_model", report_result.Model)
                    sessionStorage.setItem("vehicle_to_view_brand", report_result.Brand)
                    sessionStorage.setItem("vehicle_to_view_location", report_result.Location)
                }
                //Refund successful
                else if (report_result.message == "Successfully processed refund"){
                    //clear session storage
                    var message_to_set = "Please check your SMS for details of your refund for your vehicle " + sessionStorage.getItem("vehicle_to_view_plateno")
                    sessionStorage.clear()
                    sessionStorage.setItem("message", message_to_set)
                    window.location.href = "trip_ended.html"
                }
            }
            else{
                navigator.geolocation.getCurrentPosition(this.success, this.error)
                if (this.submission_error == false){
                    submit_to_manage_issue = {
                        "Report":{
                            "DriverID": sessionStorage.getItem("driverid"),
                            "RentalID": sessionStorage.getItem("rental_id"),
                            "PlateNo": sessionStorage.getItem("vehicle_to_view_plateno"),
                            "Outcome": this.chosen_remedy,
                            "Content": this.faultDescription
                        },
                        "Current Location": {'lat': this.lat, 'lng': this.long},
                        "PaymentID": sessionStorage.getItem("payment_intent_id"),
                        "PhoneNo": sessionStorage.getItem("mobile_number")
                    
                    }
                    console.log(submit_to_manage_issue)
        
                    const report_response = await fetch("http://localhost:5300/manage_issue",
                            
                        {
                                method: 'POST',
                                body: JSON.stringify(submit_to_manage_issue),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                        })
                    const report_result = await report_response.json()
                    console.log(report_result)
                    
                    //Replacement successful
                    //Replacement successful
                if (report_result.code != 200){
                    this.submission_error_message = report_result.message
                }
                else if (report_result.message == "Successfully processed replacement"){
                    // Display outcome on screen
                    this.outcome = "Successfully processed replacement, please go back to booking page to view new car details"
                    sessionStorage.setItem("vehicle_to_view_plateno", report_result.booking.data.PlateNo)
                    sessionStorage.setItem("vehicle_to_view_model", report_result.Model)
                    sessionStorage.setItem("vehicle_to_view_brand", report_result.Brand)
                    sessionStorage.setItem("vehicle_to_view_location", report_result.Location)
                }
                //Refund successful
                else if (report_result.message == "Successfully processed refund"){
                    //clear session storage
                    var message_to_set = "Please check your SMS for details of your refund for your vehicle " + sessionStorage.getItem("vehicle_to_view_plateno")
                    sessionStorage.clear()
                    sessionStorage.setItem("message", message_to_set)
                    window.location.href = "trip_ended.html"
                }
            
            }  
                
            }   
        },
        

    },
    created(){
        if (!"geolocation" in navigator) {
            console.log("geolocation is not available")
            this.submission_error = true
            this.submission_error_message = "Geolocation is not available"
        }
        else{
            navigator.geolocation.getCurrentPosition(this.success, this.error)
        }
        
    }
})

app.mount('#app')