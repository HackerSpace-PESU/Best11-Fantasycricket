# Best11-Fantasycricket

## Description 

In the past year or so fantasy cricket has been getting a lot of traction and with recent deal struck by Dream11 with IPL, more people are playing fantasy cricket than ever, but the problem is lot of people do not make right choices in choosing the team and end up thinking winning is all about luck and nothing else. With our project we want to break that myth by making a model which when given with players predicts the best 11 that will have the most points in the fantasy league. We have gathered statistics of players throughput their career and the model takes in the scores last 5 games a player has played and it tries to predict his score in the next game using a linear model. 

## Requirements

1. [FastAPI](https://fastapi.tiangolo.com/)
2. [sklearn](https://scikit-learn.org/stable/)
3. [scrapyrt](https://scrapyrt.readthedocs.io/en/stable/) 
4. [scrapy](https://docs.scrapy.org/en/latest/)

Install using </br>
```bash
pip3 install -r requirements.txt
```

## Local Development

To run our project follow these steps

1. Clone our repo into your system  
 
2. Change your directory to 'Best11-Fantasycricket' using
```bash
cd Best11-Fantasycricket
``` 

3.  
	**Linux and MACOS**
	
	1. Type `nano /etc/hosts` on your terminal or open `/etc/hosts` on your prefered editor 

	**Windows**
	1. Open `C:\windows\system32\drivers\etc\hosts` in your prefered editor

	
	2. And add the below line to the the file and save

	`127.0.0.1 espncricinfo`

	**OR**

	1. Open `app/fantasy_cricket/scrapyrt_client.py` in your prefered editor

	2. Change line `16` to
		
		```python
			self.url = "http://localhost:9080/crawl.json"
		```

4. Open a tab on your terminal and run 

`uvicorn app.main:app`

5. Open another tab on your terminal and run

`scrapyrt`


6. Open `http://localhost:8000/`  and voila!! 

**Note:**
Visit `http://localhost:9080/crawl.json` with the correct queries to see the crawler api 

### Docker

1. Follow the steps:

	```bash
		docker build -t espncricinfo:latest "." -f docker/espncricinfo/Dockerfile
		docker build -t best11:latest "." -f docker/11tastic/Dockerfile
		docker-compose -f docker/docker-compose.yaml up
	```

2. Visit `http://localhost:8080/` to see the website in action

**Note**
     Visit `http://localhost:9080/crawl.json` with the correct queries to see the crawler api 


## How do I contribute to this project????

:warning:  Warning! Existing contributors and/or future contributors , re-fork the repo as the commit-history has been rewritten to reduce size of the repo while cloning which makes cloning much faster than before!.

Refer to the [Contributing.md](https://github.com/HackerSpace-PESU/Best11-Fantasycricket/blob/master/.github/CONTRIBUTING.md) file of our repository 
</br></br>
If you have any suggestions for our project , do raise a issue and we will look into it and if we think it helps our project we will keep it open until its implemented by us or by anyone else 
</br></br>
If you have any questions regarding our project , you can contact any of the maintainers(info on respective profile pages) or raise a issue and we'll answer you as soon as possible.  

## Thank You 

### Maintainers
	
1. [Royston](https://github.com/lucasace)

2. [Shreyas](https://github.com/SRP457)

3. [Sammith](https://github.com/SammithSB)</br>

### Acknowledgements

1. Special thanks to [scientes](https://github.com/scientes) for allowing us to use the server to host the website

2. We would like to thank [espncricinfo](https://www.espncricinfo.com/) for their amazing website with daily updates and availabilty to scrape 

If you liked our project we would really appreciate you starring this repo.

Thank you
