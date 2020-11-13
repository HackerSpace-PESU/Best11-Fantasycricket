import os

if not os.path.exists("../../data_crawler"):
	os.makedirs("../../data_crawler/ODI")
	os.mkdir("../../data_crawler/T20")
	os.mkdir("../../data_crawler/TEST")
	open("../../data_crawler/id_names.csv", "w+").close()
	open("../../data_crawler/ODI/match_ids.csv", "w+").close()
	open("../../data_crawler/T20/match_ids.csv", "w+").close()
	open("../../data_crawler/TEST/match_ids.csv", "w+").close()
