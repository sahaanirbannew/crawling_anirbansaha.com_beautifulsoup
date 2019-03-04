from enum import unique


def get_text_from_link(link):
    # Program: Extract Text from wwww.anirbansaha.com Blog post.
    # Input: Blog post Link
    # Output: Text File.
    # Output file name: Blog post slug.
    # Output file path: C:/Users/Anirban Saha/Dropbox/Anirban - Madhu/Python Written Files/"+filename+".txt
    # Developer: Saha & Thatikonda
    # Date: 03.03.2019

    import requests
    from bs4 import BeautifulSoup

    # Path to extract details from. This should be the input to this function.
    path = link

    # Output file name.
    str_split = path.split('.com/')
    filename = str_split[1].replace('/', '')
    # print(filename)

    # Extracting information.
    page = requests.get(path)
    soup = BeautifulSoup(page.content, 'html.parser')
    list(soup.children)
    html = list(soup.children)[2]
    list(html.children)
    body = list(html.children)[3]
    para = list(body.children)[1]

    # print(para.get_text())
    texti = soup.find_all('p')
    matter = ''

    for x in texti:
        matter = matter + x.get_text()

    # print(matter)

    try:
        # print("Trying to write in the file")
        path = "C:/Users/Anirban Saha/Dropbox/Anirban - Madhu/Python Written Files/" + filename + ".txt"
        f = open(path, 'w', encoding='utf-8')
        f.write(matter)
        print("Success: " + filename)
        return path
    except:
        print("Error: " + filename)
    finally:
        f.close()


def main():
    import requests
    import regex
    from bs4 import BeautifulSoup

    # Takes User input.
    # searchterm = "cologne"
    searchterm = input("What do you want to search?").replace(' ', '+')
    # print(searchterm)

    path = "http://www.anirbansaha.com/?s=" + searchterm
    # print(path)

    page = requests.get(path)
    soup = BeautifulSoup(page.content, 'html.parser')

    html = list(soup.children)[2]
    list(html.children)
    body_code = list(html.children)[3]
    body_code = list(body_code)[1]

    searchresults = soup.find_all(id="search-results")
    search_results_ = str(searchresults).split('<article class="result">')
    linked_listi = regex.findall(r'(https?://\S+)', str(search_results_))

    link_list = []      #List to maintain log.
    index_list = []     #List to maintain complete log.

    import csv
    with open("C:/Users/Anirban Saha/Dropbox/Anirban - Madhu/Python Written Files/index.csv") as index_file:
        readCSV = csv.reader(index_file, delimiter=',')
        for row in readCSV:
            #print(row)
            index_list.append(row[1])

    # Maintains a log of all the files downloaded.
    f = open("C:/Users/Anirban Saha/Dropbox/Anirban - Madhu/Python Written Files/index.csv", 'a',
             encoding='utf-8')

    for link in linked_listi:
        link.strip()
        if 'uploads' not in link:
            link = link.split('">')[0]
            # print(link)
            if link not in link_list:
                link_list.append(link)

                index_text = searchterm + ',' + str(link)
                if link not in index_list:
                    f.write(index_text+','+get_text_from_link(link)+'\n')
                else:
                    print("Skipped.")
                    f.write(index_text + ', skipped.\n')
    f.close()

if __name__ == '__main__':
    main()
