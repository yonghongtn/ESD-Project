/* This is the Vue app for uploading QR code */
const app = Vue.createApp({
    data() {
        return {
            image_url: null,
            error_message: null
        }
    },
    methods:{
        redirect(){
            window.location.href = "booking.html"
        },
        async uploadQR(){
            const formData = new FormData();
            const fileField = document.querySelector('input[type="file"]');
            formData.append("key", "3c3c6926aff94a2eed071abb1497fd16");
            formData.append("image", fileField.files[0]);

            var response = await fetch("https://api.imgbb.com/1/upload", {method: "POST", body: formData,})
            var data = await response.json();
            console.log(data.data.url);
            this.image_url = data.data.url;

            //call parking handler microservice
            var content_body = {
                "driver_id": sessionStorage.getItem("driverid"),
                "rentalid": sessionStorage.getItem("rental_id"),
                "image": this.image_url
            }
            console.log(content_body)
            const parking_response = await fetch("http://127.0.0.1:5100/parking_handler/qrcode",
            {
                method: 'POST',
                body: JSON.stringify(content_body),
                headers: {
                    'Content-Type': 'application/json'
                },
            })
            const parking_result = await parking_response.json()
            console.log(parking_result)
            if (parking_result.code == 200){
                //clear session storage
                sessionStorage.clear()
                window.location.href = "trip_ended.html"
            }
            else{
                this.error_message = parking_result.message
            }

                
        }
    }
})

app.mount('#app')