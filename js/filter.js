const app = Vue.createApp({
    data() {
        return {
            /* Chosen variables */
            location_selected : "All",
            filter_selected : "Choose filter",

            /* Variable options */
            locations : ["All", "SCIS", "LKCSB", "SOSS"],
            filters: ["Choose filter","Brand","Model","Ascending Price","Descending Price"],

            /* Data for Vehicles*/
            /* This is data obtained from HTTP GET from microservice */
            vehicles : [
                {plateNo: "S1234567A", brand: "Toyota", model: "Vios", location: "SCIS", price: 1000},
                {plateNo:"S1234567B", brand: "Honda", model: "City", location: "SCIS", price: 2000},
                {plateNo:"S1234567C", brand: "Toyota", model: "Altis", location: "LKCSB", price: 3000},
                {plateNo:"S1234567D", brand: "Honda", model: "Accord", location: "LKCSB", price: 4000},
                {plateNo:"S1234567E", brand: "Toyota", model: "Vios", location: "SOSS", price: 5000}
            ],
        }
    },
    computed:{
        displayedVehicles(){
            /* Filter by location, then by selected filter */
            var to_return  = []
            if(this.location_selected == "All"){
                to_return = this.vehicles
            }
            else{
                for(var i = 0; i < this.vehicles.length; i++){
                    if(this.vehicles[i].location == this.location_selected){
                        to_return.push(this.vehicles[i])
                    }
                }
            }
            if(this.filter_selected == "Choose filter"){
                return to_return
            }
            else if(this.filter_selected == "Brand"){
                return to_return.sort((a,b) => (a.brand > b.brand) ? 1 : -1)
            }
            else if(this.filter_selected == "Model"){
                return to_return.sort((a,b) => (a.model > b.model) ? 1 : -1)
            }
            else if(this.filter_selected == "Ascending Price"){
                return to_return.sort((a,b) => (a.price > b.price) ? 1 : -1)
            }
            else if(this.filter_selected == "Descending Price"){
                return to_return.sort((a,b) => (a.price < b.price) ? 1 : -1)
            }
        }
    },
    methods: {
        showDetails(vehicle){
            /* Set session storage to vehicle to view */
            console.log(vehicle)
            sessionStorage.setItem("vehicle_to_view_plateno", vehicle.plateNo)
            sessionStorage.setItem("vehicle_to_view_brand", vehicle.brand)
            sessionStorage.setItem("vehicle_to_view_model", vehicle.model)
            sessionStorage.setItem("vehicle_to_view_location", vehicle.location)
            sessionStorage.setItem("vehicle_to_view_price", vehicle.price)
            /* Redirect to view vehicle page */
            window.location.href = "cardetails.html"
        }
    }
});

app.mount('#app');


