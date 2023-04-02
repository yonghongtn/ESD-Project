Pre- Set Up

Step 1:
Set up enivronment variables for Account SID & Account Token

How:
1. Windows + R  
2. Key in sysdm.cpl
3. On the tab choose advance then environment variables
4. Under user variable click "new"
5. 
Variable Name: TWILIO_ACCOUNT_SID
Variable Value: AC70575cc9cacf0a4c926ee2ec594f666a

Variable Name: TWILIO_AUTH_TOKEN 
Variable Value: 2e860aa08d797df3473daa11ce8b0886

6. Check if variable is in system
In CMD, key in echo %TWILIO_ACCOUNT_SID%
see if the value appears
Do the same for TWILIO_AUTH_TOKEN [echo %TWILIO_AUTH_TOKEN%]

Step 2:
Download Twilio 
1. Pip install twilio
