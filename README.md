# Installation and Running the Project
1. Ensure wamp is installed and turned on
2. Copy the whole repository folder into C:\wamp64\www and rename the folder to ‘ESDProject’
3. Run script.sql to load the 4 databases
4. In phpmyadmin (http://localhost/phpmyadmin), create a new account is213 with no password, with the rights to read, edit, insert (tick all 5 conditions)
5. Open docker and log in
6. Delete any existing rabbitmq containers and images
6. In the docker-compose.yaml file in the ‘dockercompose’ folder, change to your twilio credentials obtained from the Twilio console such as the Account_SID, Auth Token and the Twilio phone number and replace all usernames with your own docker username.
7. In setsessionstorage.js in the js folder, change the name and 	phone number to that of yours
8. Open a new terminal and set the directory to that of the ‘dockercompose’ folder, ensuring that the current path is C:\wamp64\www\ESDProject\dockercompose (cd dockercompose)
9. Enter the command “docker-compose build”, followed by “docker-compose up” to build the images and run containers
10. Open the web browser and type localhost/ESDProject and you should see the starting page


# Twilio Setup
1. Sign up for a twilio account at https://www.twilio.com/
2. Go to Console and click on ‘get a phone number’
3. Go to the docker-compose.yml file located in the ‘dockercompose’ folder of the ESDProject
4. The account credentials are located in the Account Info in the Twilio console. 
