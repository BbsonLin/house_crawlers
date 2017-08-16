import os
import subprocess

if __name__ == '__main__':
    results_folder = "./results/"
    if not os.path.exists(results_folder):
        print("You don't have results folder ...")
        print("Automatically generate it ...")
        os.mkdir(results_folder)
    for i in range(1, 27):
        subprocess.run(["scrapy", "crawl", "saleInfo", "-a",
                        "regionid={}".format(i), "-o",
                        "./results/sale{}.json".format(i)],
                       stdout=subprocess.PIPE)
