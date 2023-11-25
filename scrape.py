from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os

Titles = []
Date = []
Links = []
Likes =[]

def scrape_page(url):
    try:
        # Make a GET request to the specified URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            response = requests.get(url, headers=headers)
        except:
            print("Unable to fetch page with url:",url)
            return

        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all article elements with the specified class
            articles = soup.find_all('article', class_='blog-item')

            for article in articles:
                # Extract title
                title = article.find('h6').text.strip()

                # Extract likes
                likes_element = article.find('a', class_='zilla-likes')
                likes = likes_element.text.split()[0] if likes_element else '0'

                # Check if the article has an image
                has_image_class = 'with-image' in article.get('class', [])

                # Extract image link
                image_link = article.find('a', class_='rocket-lazyload')['data-bg'] if has_image_class else 'N/A'

                # Extract date
                date_element = article.find('div', class_='bd-item').find('span')
                date = date_element.text if date_element else 'N/A'
                
                # Adding info in lists
                Titles.append(title)
                Links.append(image_link)
                Date.append(date)
                Likes.append(likes)

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")

    except Exception as ex:
        print("Unable to scarpe page with url:",url)



def scrape_last_page_number(url):
    # Make a GET request to the specified URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
    except:
        print("Unable to fetch page with url:",url)
        return



    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the last element with the class "page-number"
        last_page_number_element = soup.find_all(class_='page-numbers')[-2]

        # Extract the page number from the element
        if last_page_number_element:
            last_page_number = int(last_page_number_element.text)
            print(f"The last page number is: {last_page_number}")
            return last_page_number
        else:
            print("No element with class 'page-numbers' found on the page.")
            return -1

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":

    start_time = time.time()

    #this is the base url of the website
    base_url = "https://rategain.com/blog"

    # Create a folder to store the output files
    output_path = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Get the last page number
    last_page_number = scrape_last_page_number(base_url)

    # Scrape all pages
    for page_num in range(1, last_page_number + 1):
        url = f"{base_url}/page/{page_num}/"
        print(f"Scraping page {page_num}...")
        scrape_page(url)



    # Create a Pandas dataframe from the data
    df = pd.DataFrame({'Title': Titles, 'Date': Date, 'Likes': Likes, 'ImageLinks': Links})

    # Save the dataframe to a CSV file
    output_file_path = os.path.join(output_path, 'blog.csv')
    df.to_csv(output_file_path, index=False)

    end_time = time.time()
    print(f"Time taken to scrape the page: {end_time - start_time:.2f} seconds")