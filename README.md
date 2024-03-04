## Example for Docker Build Secret  
### Use case: Create a simple HTTP web-server that exposes an endpoint /sum that accepts POST requests. The data of the request should be a JSON of the form { "num1": 2, "num2": 2 } and the response should contain the sum. Extract the addition method into a separate library and consume it as a dependency in the web-server application. Bundle the above web server into a Docker image and run it.

### Let's solve this problem step-by-step:

#### Steps:
1. Create a new private git repository for packaging python library
2. Create a new python-flask application which will consume the python package
3. Write a Dockerfile for the to bundle the application in docker image.
4. Use Docker build secret

##### Step 1: Create a private git repository with name "akmaddition"
Refer the private repo: https://github.com/vishal-meshram/akmaddition.git

##### Step 2: Create a new python-flask application which will consume the python package.
This current repo is to consume the private git repo.

``` bash
mkdir consume-akmaddition
cd consume-akmaddmition

python3 -m venv env
source env/bin/activate

pip install flask             // install the flask
pip install -U flask-openapi3 // install Flask OpenAPI3 web API framework 
pip install git+https://github.com/vishal-meshram/akmaddition.git //install akmaddition package
//This will ask you username and password. Provide git username and 
//persoanl access token as password.
```
##### To Run this applciation without Docker:
```bash
python3 app.py
```
![alt text](images/1_app%20output.png)

##### Open the link in the browser:
```
http://127.0.0.1:9000/openapi
```
##### Click on "Swagger"
![alt text](images/2_swagger%20app%20output.png)



##### Click on "Try it out" and enter values for "num1": 2, "num2" : 5 and click on "Execute" and check the output.
![alt text](images/3_test%20api.png)


### Step 3: Dockerize this application using Docker build secret
Since we're utilizing a private Git repository containing our Python package, namely "akmaddition," the primary hurdle in Dockerizing this application is concealing the GitHub personal access token and generating a Docker image without disclosing the token. Now, we'll employ Docker build secrets to tackle this challenge.

#### Prerequisite:
1. Docker must be installed
2. Generate a Personal Access Token (Classic) in your GitHub account.

Steps: Login GitHub account -> Profile Avtar -> settings -> Developer- settings -> Personal access tokens -> Tokens (classic) -> Generate new token

```bash
$ echo ".git-credentials" >> .gitignore
$ echo "https://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:x-oauth-basic@github.com" > .git-credentials
// Instead of this "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", use your personal access token here..
```

##### Create a image from Dockerfile by using command:
```bash
docker build --secret id=gitcredentials,src=.git-credentials -t app .
```

##### check the docker images and create container
![alt text](images/4_docker_images.png)

##### create a container from image "app"
```bash
docker run -d -p 8000:9000 app
```
##### check the status of the container using command: 
```bash
docker ps
```
![alt text](images/5_Docker_ps_command.png)

### Congratulations!!! your container is running at port 8000

##### visit the browser and give command and test your application.
```bash
http://localhost:8000/openapi/
```
![alt text](images/6_output.png)
