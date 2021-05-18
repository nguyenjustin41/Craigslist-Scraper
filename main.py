from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import os
import smtplib
from email.message import EmailMessage


# Set Options for headless mode to be true
options = Options()
options.headless = True

# Handler for when headless mode is True, this opens a 1920x1200 window-size to reveal it
options.add_argument("--window-size=1920,1200")

# Path to where chromedriver is located
DRIVER_PATH = "C:\\Webdrivers\\chromedriver"

# URL to go web scrape
BASE_URL = 'https://losangeles.craigslist.org'

# To switch between filtering specific keywords vs just 10 of the most recent items with no specific search
    # 
    # NUM_STR = '10'
    # SEARCH = NUM_STR + ' Most Recent'
    # keyword that we will filter out
    # 
# To search only a specific keyword
SEARCH = "tools"

# creating a webdriver object taking arguments for options and path
# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# ChromeDriverManager().Install() installs the latest webdriver so you don't run into compatibility issues
# if your google chrome updates on your machine
driver= webdriver.Chrome(ChromeDriverManager().install(), options=options)

# Opens up the craigslist free page
driver.get(BASE_URL + '/search/zip')

# holds the total posts
total_Posts = []
filtered_Posts = []

# I used start and end to determine how fast the program can iterate and scrape each page compared to the Recursive way 
# The iterative while loop was faster so that's why the recursive way got commented out below
# start = time.time()

# paginate through the 'next page' anchor tag until anchor tag is None 
while (True):
    # initialize Beautiful Soup (so we can use soup.find)
    soup = BeautifulSoup(driver.page_source, 'html.parser') 
    # scrape anchor tag for next button
    nextPage = soup.find('a', class_='next')
    # stop if we can't find an anchor tag with the class of 'next'
    if nextPage is None: break
    # shove all titles into end of posts list of that exact page
    total_Posts.extend(soup.find_all('li', class_='result-row'))
    # scrape the href of the nextpage anchor tag
    pageLink = nextPage.get('href')
    # open craigslist website with nextpage href
    driver.get(BASE_URL + pageLink)
# end = time.time()
   
# This is an alternative way to loop over 
filtered_Posts = [post for post in total_Posts if SEARCH.lower() in post.find('a', class_='result-title').get_text().lower()]


# iterate over every post element and scrape the title, Date/Time, and URL 
def outputResults(posts):
    # You can use this extra array if you want to filter by specific # of elements before sending
    # before_Final_Result = []  
    
    # holds all scraped results
    final_Result = []
  
    # tells me how many posts were scraped out of ALL posts on craigslist free
    print(f"--{len(posts)} {SEARCH} scraped out of {len(total_Posts)} posts.")
    # enumerate/loop over every post and collect the post title, post url, and post time (w.o microseconds)
    for i, post in enumerate(posts):
        titleDiv = post.find('a', class_='result-title')
        postTitle = titleDiv.get_text() 
        postURL = titleDiv.get('href')
        postTimeText = post.find('time').get('datetime')
        # formatted as: 2021-01-14 08:44
        # strptime converts string to datetime
        postTime = datetime.strptime(postTimeText, '%Y-%m-%d %H:%M')
        
        dtNow = datetime.now() 
        # subtracts microseconds from the sent time
        x = dtNow - timedelta(microseconds=dtNow.microsecond)
        ellapsedTime = (x - postTime)


        final_Result.append(f'> {postTitle} \n  {ellapsedTime}  \n {postURL}\n \n')
        print(f'{i}: {postTitle}: {ellapsedTime}: {postURL}')
    
    # if before_Final_Result array scrapes 0 results
    if len(final_Result) == 0:
        no_results = ['No Matching Results']
        return no_results
    
    # if you want to filter the to a hardcoded # of items you can append into the before_Final_Result array first
    # and then append the # of elements to the final_Result using this code below
    # make sure you also change the final_Result.append(f'> {postTitle} \n  {ellapsedTime}  \n {postURL}\n \n') to
    # before_Final_Result.append(f'> {postTitle} \n  {ellapsedTime}  \n {postURL}\n \n'), then uncomment the line below to configure
    # else:
    #     for i in range(3):
    #         final_Result.append(before_Final_Result[i])             
    
    return final_Result

# converts list to string to send off to email as a string
def listtoString(s):
    str1 = ""
    return str1.join(s)

# CHANGE argument to filtered_Posts for a filtered search result
# CHANGE argument to total_Posts for a list of most recent general things
final_Result_Array = outputResults(filtered_Posts)

# convert from list to string
final_Result_String = listtoString(final_Result_Array)

print(final_Result_String)

driver.quit()

# Hides the emails and password that I will be sending the free items to
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_ADDRESS2 = os.environ.get('EMAIL_USER2')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
# Email recipients
recipients = [EMAIL_ADDRESS, EMAIL_ADDRESS2]

print(EMAIL_ADDRESS)
print(EMAIL_ADDRESS2)

# function that creates the email and sends it using smtpblib 
def send_mail():
    if final_Result_String == 'No Matching Results':
        print('Email not sent')
        return 
    # creating the actual email message
    msg = EmailMessage()
    msg['Subject'] = f'{SEARCH} Scraped'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipients
    msg.set_content(final_Result_String)


    # open a file object that reads, then closes automatically (with as statement) 
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # logs me into the email sender account
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        # sends the message from that email account
        smtp.send_message(msg)

    print("EMAIL SENT")

send_mail()



# Alternative pagination on cragislist free using Recursion (the other one used a while loop)

# start = time.time()
#  def stepThroughPages(posts, pageLink):
#      driver.get(BASE_URL + pageLink)
#      soup = BeautifulSoup(driver.page_source, 'html.parser') 
#      nextPage = soup.find('a', class_='next')
#      # BASE CASE FOR RECURSION
#      if nextPage is None: return posts
#      # Adds all .text (title) of each anchor tag to the end of array posts
#      posts.extend(soup.find_all('a', class_='result-title'))

#      return stepThroughPages(posts, nextPage.get('href'))

#  totalPosts = stepThroughPages([], '/search/zip')
#  end = time.time()

# I used these print statements to tell me whether recursion or while loop was faster 
# when paginating across each page of craigslist free  
# """
#  print(f"runtime: {end - start}")
#  print(len(totalPosts))
# """

