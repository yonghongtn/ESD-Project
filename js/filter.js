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
            vehicles : [],
        }
    },
    computed:{
        displayedVehicles(){
            var to_return = []
            /* Include only all vehicles whose VehicleStatus is Available*/
            for (vehicle of this.vehicles){
                if (vehicle.VehicleStatus == "Available"){
                    to_return.push(vehicle)
                }
            }
            /* Filter by location, if All do not do further filtering*/
            if (this.location_selected != "All"){
                to_return = to_return.filter(vehicle => vehicle.ParkingSpotName == this.location_selected)
            }
            /* Filter by filter, if Choose filter do not do further filtering*/
            if (this.filter_selected == "Brand"){
                to_return = to_return.sort((a,b) => (a.Brand > b.Brand) ? 1 : ((b.Brand > a.Brand) ? -1 : 0))
            }
            else if (this.filter_selected == "Model"){
                to_return = to_return.sort((a,b) => (a.Model > b.Model) ? 1 : ((b.Model > a.Model) ? -1 : 0))
            }
            else if (this.filter_selected == "Ascending Price"){
                to_return = to_return.sort((a,b) => (a.Price > b.Price) ? 1 : ((b.Price > a.Price) ? -1 : 0))
            }
            else if (this.filter_selected == "Descending Price"){
                to_return = to_return.sort((a,b) => (a.Price < b.Price) ? 1 : ((b.Price < a.Price) ? -1 : 0))
            }
            return to_return
        }
    },
    methods: {
        showDetails(vehicle){
            /* Set session storage to vehicle to view */
            //console.log(vehicle)
            sessionStorage.setItem("vehicle_to_view_plateno", vehicle.PlateNo)
            sessionStorage.setItem("vehicle_to_view_brand", vehicle.Brand)
            sessionStorage.setItem("vehicle_to_view_model", vehicle.Model)
            sessionStorage.setItem("vehicle_to_view_location", vehicle.ParkingSpotName)
            sessionStorage.setItem("vehicle_to_view_price", vehicle.Price)
            sessionStorage.setItem("vehicle_to_view_priceid", vehicle.PriceID)
            sessionStorage.setItem("vehicle_to_view_location_id", vehicle.ParkingSpotID)
            /* Redirect to view vehicle page */
            window.location.href = "cardetails.html"
        }
    },
    created(){
        /* Get data from microservice */
        $(async() => {           
            // Change serviceURL to your own
            var serviceURL = "http://localhost:5003/rentalvehicle";

            try {
                const response =
                 await fetch(
                   serviceURL, { method: 'GET'}
                );
                const result = await response.json();
                 if (response.status === 200) {
                    // success case
                    var vehicles = result.data.vehicles; //the array is in vehicles within data of 
                    this.vehicles = vehicles
                    console.log(vehicles)
                    //find the list of possible locations in this.vehicles
                    var locations = ["All"]
                    for (vehicle of vehicles){
                        if(!locations.includes(vehicle.ParkingSpotName)){
                            locations.push(vehicle.ParkingSpotName)
                        }
                    }
                    //console.log(locations)
                    this.locations = locations
                }
            }
            catch (error) {
                console.log(error);
            }
        })
    }
});

app.mount('#app');


