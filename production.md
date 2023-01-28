
## Setting up Authentication

The application uses Google open auth 2.0 to authenticate users. Therefore, we need to register application in Google
and set it up. Follow below steps to register and set it.

### Register application in Google
Follow steps provided in below link to create/register application in Google
https://geekyhumans.com/how-to-implement-google-login-in-flask-app/

### Enable Authentication in environment variables.

set value of "AUTH_ENABLED" to "true".
set value of "REDIRECT_URL" to DNS of the application. For local testing set it to "http://127.0.0.1:8080/callback"
Download the client_secret.json from the Google application registered and copy to
web/client_secret.json

add valid email address as admins
```
./manage.py add-admin-member -e <you_email> -n <name>
```

### Disable Authentication
If working on local, disable Authentication.
Note that when Authentication is disabled, the user is always set as "itrust_test@gmail.com"

### Adding admin users to the application who have access to all operations.

## Bring up the docker application in prod account
### Create the instance in GCP / AWS / digital ocean

One thing to notice is that the perfomance sucks in instance with 1GB RAM. it is recommended to have more than that.

### Bringup the application

## Creating Core members.

Admin can now create themselves and other core members in the application using create operation.