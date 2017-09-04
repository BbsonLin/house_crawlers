import os
import subprocess
import pyrebase
import json

if __name__ == '__main__':

    config = {
        "apiKey": "AIzaSyAvPSQcgk1c8xm_FEfUW94KtWi95cKR7-g",
        "authDomain": "house591-d2bd1.firebaseapp.com",
        "databaseURL": "https://house591-d2bd1.firebaseio.com/",
        "storageBucket": "house591-d2bd1.appspot.com",
    }

    # All Environment data
    regions = [1,2,3,4,5,6,7,8,10,11,12,13,14,15,17,19,21,22,23,24,25,26]
    results_folder = "./results/"
    log_folder = "./log/"

    # Make results folder
    if not os.path.exists(results_folder):
        print("You don't have results folder ...")
        print("Automatically generate it ...")
        os.mkdir(results_folder)

    # Make log folder
    if not os.path.exists(log_folder):
        print("You don't have log folder ...")
        print("Automatically generate it ...")
        os.mkdir(log_folder)

    # Initialize Firebase
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    # Crawl all regions of 591
    print("Crawling all Houses ...")
    for i in regions:
        print("Crawling Region {} ...".format(i))
        subprocess.run(["scrapy", "crawl", "saleInfo", "-a",
            "regionid={}".format(i), "-o",
            "{}saleInfo{}.json".format(results_folder, i)],
            stdout=subprocess.PIPE)

        data=""
        with open("{}saleInfo{}.json".format(results_folder, i), "r") as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError:
                continue

        # Insert data into firebase
        db.child("house_591").child("sale").child(i).set(data)

        # Change result files to log files
        os.rename("{}saleInfo{}.json".format(results_folder, i), "{}saleInfo{}.json".format(log_folder, i))

