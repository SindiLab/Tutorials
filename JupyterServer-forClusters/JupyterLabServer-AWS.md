
# Setting Up a Jupyter Server on a Cluster or Instance 

The Jupyter framework provides a nice a framework for developing and evaluating models. More specifically, using Jupyter Lab will allow one to code in terminal/text editor, compile and run codes with ease and use of GUI. In this short tutorial, we will go over how to set up a Jupyter Lab server on a remote machine; for this document we will set up a Jupyter Lab server on an AWS EC2 instance running Ubuntu. 

### These Steps are Done on the Remote Machine
#### Step 1: Set a Password for Logging in

````bash
$ jupyter notebook password
````

which will prompt you with fields to enter and confirm your password. You will use this password to log-in when you connect to the server.

#### Step 2: Create a SSL Certificate
Next we will create a self-assigned Secure Sockets Layer (SSL) certificate. The directory in which the certificate is created in will be the directory that you will have access to when using Jupyter. 
1. Change directory to the approprtiate directory 
````bash
$ cd ~
```` 

2. Creating a self-signed ssl certificate with `openssl`. In the following example, we create a certificate good for 500 days with both the key and certificate data written to the same file:
````bash
$ openssl req -x509 -nodes -days 500 -newkey rsa:2048 -keyout key4Jupyter.key -out cert4Jupyter.pem
```` 
***keep in mind that when you create the open certificate, your browser may ask you about authenticating the connection. Make sure to do so when prompted by your browser***. For more information about how to create a certified SSL certificate, checkout [This tutorial](https://arstechnica.com/information-technology/2009/12/how-to-get-set-with-a-secure-sertificate-for-free/).

3. Remember the path for both the key and the certificate created. In the example above, we would have
````bash
$ KEY_PATH="~/key4Jupyter.key"
$ CERT_PATH="~/cert4Jupyter.pem"
````

#### Step 3: Start Jupyter Server on the Remote Machine
Now having the path for both the key and the certificate, we can start the Jupyter :
````
$ jupyter lab --certfile=$KEY_PATH --keyfile $CERT_PATH
````

#### Step 4: Choose a Port
Now we have to make sure that your desired port, usually 8888, is open and available. If you don't know what is listening on or using port 8888, you can run the following to kill anything that is currently running
````
$ lsof -ti:8888 | xargs kill -9
````

### These Steps are Done your Local Machine

#### Step 5: Configure the Local Client 
For this step, we need to SSH into the remote machine where we set up the Jupyter server, to serve as a bridge between our machine and the remote one. We will configure our local client for connecting to an EC2 instance using:
````bash
$ ssh -i `~/EC2KEYPAIR.pem` -N -f -L 8888:localhost:8888 ubuntu@EC2-IP-ADDRESS.compute-1.amazonaws.com
````

after this step we are done! Once again, remember that since we created an open SSL certificate, you browser might show that the page is not secure. Make sure to select "advance" or "more details" options and select an option which will allow you to proceed to the page. 

*Enjoy your new Jupyter Server :)*
