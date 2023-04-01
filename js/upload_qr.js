/* This is the Vue app for uploading QR code */
const app = Vue.createApp({
    data() {
        return {
            image_url: null,
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
        }
    }
})

app.mount('#app')