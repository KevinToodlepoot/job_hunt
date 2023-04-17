import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from company_dictionaries import companies, js_companies, no_listing_companies

def generate_motivation():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.environ["GPT_KEY"]}'
    }

    data = {
        "model": "text-davinci-003",
        "prompt": "Cheerful, two-sentence inspiration!",
        "temperature": 1,
        "max_tokens": 50,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)

    if response.status_code == 200:
        generated_text = response.json()['choices'][0]['text']
    else:
        print(f'Error reaching openai: {response.status_code}')
        generated_text = "Here’s a little motivational message. We’ll keep it short and sweet and cheery!"

    return generated_text

color_scheme = {
    'background': 'D9D9D9',
    'container': 'FFF',
    'text': '000',
    'links': '8B0000',
    'quote': '858585',
}

def send_email_ses(job_openings_by_company):
    ses_client = boto3.client('ses')

    subject = 'Job Openings'

    message = generate_motivation()

    body_html = f"""
    <html>
       <body style="background-color: #{color_scheme['background']};text-align: center;font-family: Optima;">
            <div class="container" style="background-color: #{color_scheme['container']};margin: auto;width: 80%;padding: 20px;">
	            <div class="header" style="text-align: left;margin-left: 20px;">
		            <h1 style="font-family: TimesNewRoman, serif;color: #{color_scheme['text']};">Hey Kevin,</h1>
    	                <p style="font-family: Optima;">Here’s your weekly job search update!</p>
	            </div>
                <div class="quote" style="font-family: Optima;color: #{color_scheme['quote']};padding-left: 25%;padding-right: 25%;">
    	            <hr style="margin: 20px auto;width: 50%;">
    	            <em>{message}</em>
                    <hr style="margin: 20px auto;width: 50%;">
                </div>
                <div class="content" style="font-family: Optima;">
    """

    for company_name, job_openings in job_openings_by_company.items():
        company_url = job_openings[0][1]
        body_html += f'<a href="{company_url}" style="color: #{color_scheme["links"]};text-decoration: none;"><h2 style="font-family: TimesNewRoman, serif;">{company_name}</h2></a>'
        for job, _ in job_openings:
            body_html += f'<p style="font-family: Optima;">{job}</p>'
        body_html += f'<hr style="margin: 20px auto;width: 80%;">'

    body_html += f"""
                </div>
                <div class="header" style="text-align: left;margin-left: 20px;">
    	            <h1 style="font-family: TimesNewRoman, serif;color: #{color_scheme['text']};">Check these out!</h1>
                    <p style="font-family: Optima;">These are jobs that can't be scraped by the program.</p>
                </div>
    """

    for company_name, company_data in js_companies.items():
        company_url = company_data['url']
        body_html += f'<a href="{company_url}" style="color: #{color_scheme["links"]};text-decoration: none;"><p style="font-family: Optima;">{company_name}</p></a>'

    body_html += f"""
                <hr style="margin: 20px auto;width: 80%;">
                <div class="header" style="text-align: left;margin-left: 20px;">
    	            <h1 style="font-family: TimesNewRoman, serif;color: #{color_scheme['text']};">Also these!</h1>
                    <p style="font-family: Optima;">These are jobs that didn't have listings to base the scraping off of.</p>
                </div>
    """

    for company_name, company_data in no_listing_companies.items():
        company_url = company_data['url']
        body_html += f'<a href="{company_url}" style="color: #{color_scheme["links"]};text-decoration: none;"><p style="font-family: Optima;">{company_name}</p></a>'

    body_html += """
            </div>
        </body>
    </html>
    """

    try:
        response = ses_client.send_email(
            Source = os.environ['FROM_EMAIL'],
            Destination = {
                'ToAddresses': [os.environ['TO_EMAIL']]
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': body_html}}
            }
        )
    except ClientError as e:
        print(f"Error: {e}")
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")

# ======================================================

def check_job_openings(url, parse_function):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    job_openings = parse_function(soup)
    return job_openings

# ======================================================

def lambda_handler(event, context):
    job_openings_by_company = {}

    for company_name, company_data in companies.items():
        current_job_openings = check_job_openings(company_data['url'], company_data['parse_function'])

        print(f"{len(current_job_openings)} job openings found for {company_name}")
        
        # Only include the company if there are job openings
        if current_job_openings:
            job_openings_formatted = [(job, company_data['url']) for job in current_job_openings]
            job_openings_by_company[company_name] = job_openings_formatted

    if job_openings_by_company:
        send_email_ses(job_openings_by_company)
        print(f"Job openings found. Email sent.")
