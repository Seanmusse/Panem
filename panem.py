from bs4 import BeautifulSoup
from tqdm import tqdm
import requests 
import sys

CraigslistBaseURL = "https://www.craigslist.org/about/sites"
r = requests.get(CraigslistBaseURL)
soup = BeautifulSoup(r.text, "lxml")


CraigslistCityLinks = [] # URLs for all of the cities on the main Craigslist page (US; Canada; Europe; Asia, Pacific and Middle East; Oceania; Latin America and Caribbean; Africa)
for countries in soup.findAll("div", {"class": "colmask"}): # Iterates through each country
    for city in countries.findAll("a"): 
        CraigslistCityLinks.append(city["href"]) # Adds links of all cities to var


print(len(CraigslistCityLinks))
CraigslistJobsURLs = [] # URLs for the sections under the "jobs" header on the Craigslist website
CraigslistGigsURLs = [] # URLs for the sections under the "gigs" header on the Craigslist website
opportunitiesURLs = []

def jobs(city): #Will get all jobs in job-titles.md
    city_r = requests.get(city)
    print(city)
    city_soup = BeautifulSoup(city_r.text, "lxml")
    jobs = city_soup.find("ul", {"id": "jjj0"})
    for job in jobs.findAll("a"):
        CraigslistJobsURLs.append(city + job["href"][1::])
    
    gigs_left = city_soup.find("ul", {"id": "ggg0", "class": "left"}) # The gig section was weirdly developed, it must be separated into left and right to be scrapeable
    for gig in gigs_left.findAll("a"):
        CraigslistGigsURLs.append(city + gig["href"][1::]) # Making a valid link and adding it to var
    gigs_right = city_soup.find("ul", {"id": "ggg1"})
    for gig in gigs_right.findAll("a"):
        CraigslistGigsURLs.append(city + gig["href"][1::])

    allOpportunityURLs = CraigslistJobsURLs + CraigslistGigsURLs
    for link in tqdm(allOpportunityURLs): 
        opportunity_r = requests.get(link)
        opportunity_soup = BeautifulSoup(opportunity_r.text, "lxml")
        opportunites = opportunity_soup.find("ul", {"class": "rows"})
        for opportunitylink in opportunites.findAll("a", {"class": "result-title"}):
            opportunitiesURLs.append(opportunitylink.text)
            opportunitiesURLs.append(opportunitylink["href"])
        for opportunitylink in opportunites.findAll("a", {"class": "result-image"}):
            opportunitiesURLs.append(opportunitylink.text)
            opportunitiesURLs.append(opportunitylink["href"])

    
    for i in opportunitiesURLs: 
        print(i)

if len(sys.argv) > 1: 
    for arg in sys.argv[1::]: 
        jobs(arg)
else: 
    for i in CraigslistCityLinks:
        jobs(i)