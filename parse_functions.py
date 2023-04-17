from bs4 import BeautifulSoup

def eventide(soup):
    job_opening_elements = soup.find_all('summary', class_='wp-block-coblocks-accordion-item__title')
    
    job_openings = []
    for element in job_opening_elements:
        job_title = element.find('strong').text.strip()
        job_openings.append(job_title)

    return job_openings

def sonible(soup):
    job_opening_elements = soup.find_all('a', class_='pdf-link')
    
    job_openings = []
    for element in job_opening_elements:
        job_title = element.text.strip()
        job_openings.append(job_title)

    return job_openings

def greenhouse(soup):
    job_opening_elements = soup.find_all('div', class_='opening')
    
    job_openings = []
    for element in job_opening_elements:
        job_title = element.find('a').text.strip()
        job_openings.append(job_title)

    return job_openings

def spectrasonics(soup):
    job_opening_elements = soup.find_all('div', class_='slot')
    
    job_openings = []
    for element in job_opening_elements:
        job_title = element.find('span').text.strip()
        job_openings.append(job_title)

    return job_openings

def sonnox(soup):
    job_opening_elements = soup.find_all('h2')
    
    job_openings = []
    for element in job_opening_elements:
        job_title = element.text.strip()
        job_openings.append(job_title)

    return job_openings

def soundtoys(soup):
    job_opening_elements = soup.find_all('p', attrs={'dir': 'ltr'})
    
    job_openings = []
    for element in job_opening_elements:
        b_tag = element.find('b')
        if b_tag is not None:
            a_tag = b_tag.find('a')
            if a_tag is not None:
                job_title = a_tag.text.strip()
                job_openings.append(job_title)

    return job_openings

def apogee(soup):
    job_openings_elements = soup.find_all('li', class_='elementor-icon-list-item')

    job_openings = []
    for element in job_openings_elements:
        job_title = element.find(class_='elementor-icon-list-text').text.strip()
        job_openings.append(job_title)

    return job_openings

def ableton(soup):
    job_openings_elements = soup.find_all('li', class_='page-jobs__department__listing__item')

    job_openings = []
    for element in job_openings_elements:
        job_title = element.find(class_='has-arrow').text.strip()

        job_openings.append(job_title)

    return job_openings

def motu(soup):
    job_openings_elements = soup.find_all('a', class_='stylized-link')

    job_openings = []
    for element in job_openings_elements:
        job_title = element.text.strip()

        job_openings.append(job_title)

    return job_openings

def reason_xln(soup):
    job_openings_elements = soup.find_all(class_='flex flex-col py-6 text-center sm:px-6 hover:bg-gradient-block-base-bg focus-visible-company focus-visible:rounded')

    job_openings = []
    for element in job_openings_elements:
        job_title = element.find('span').text.strip()

        job_openings.append(job_title)

    return job_openings