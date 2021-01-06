# Best11-Fantasycricket

## Description 

In the past year or so fantasy cricket has been getting a lot of traction and with recent deal struck by Dream11 with IPL, more people are playing fantasy cricket than ever, but the problem is lot of people do not make right choices in choosing the team and end up thinking winning is all about luck and nothing else. With our project we want to break that myth by making a model which when given with players predicts the best 11 that will have the most points in the fantasy league. We have gathered statistics of players throughput their career and the model takes in the scores last 5 games a player has played and it tries to predict his score in the next game using a linear model. 

## Requirements

1. [FastAPI](https://fastapi.tiangolo.com/)
2. [sklearn](https://scikit-learn.org/stable/)
3. [pycricbuzz](https://github.com/codophobia/pycricbuzz) 
4. [scrapy](https://docs.scrapy.org/en/latest/)

Install using </br>
```bash
pip3 install -r requirements.txt
```

## I want to run your project

To run our project follow these steps

1. Clone our repo into your system  
 
2. Change your directory to 'Best11-Fantasycricket' using
```bash
cd Best11-Fantasycricket
``` 

3. Run the model : 

`uvicorn app.main:app`

5. `Open http://localhost:8000/`  and voila!! 

### Docker

1. Follow the steps:
	```bash
	docker build -t best11fantasycricket:latest "." 
	```

	```bash
	docker-compose up
	```

2. Visit `http://localhost:8080/`


## How do I contribute to this project????

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

1. Special thanks to [scientes](https://github.com/scientes) for setting up the basic webcrawler

2. We would like to thank [Howstat](http://www.howstat.com/cricket/home.asp) for their amazing website with daily updates and availabilty to scrape 

If you liked our project we would really appreciate you starring this repo.

Thank you
