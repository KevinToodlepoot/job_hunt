import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
from bs4 import BeautifulSoup
from company_dictionaries import companies, js_companies, no_listing_companies

color_scheme = {
    'background': 'BBB',
    'container': 'FFF',
    'text': '444',
    'links': '6C3E3C',
    'line': '999',
}

def send_email_ses(job_openings_by_company):
    ses_client = boto3.client('ses')

    subject = 'Job Openings'

    body_html = f"""
    <html>
        <body style="background-color: #{color_scheme['background']}; font-family: Georgia, serif;">
            <div style="background-color: #{color_scheme['container']}; margin: auto; width: 80%; padding: 20px; text-align: center;">
                <h1 style="color: #{color_scheme['text']};">Job Openings</h1>
                <hr style="border: 0; height: 3px; background-color: #{color_scheme['line']}; width: 50%; margin: 20px auto;">
    """

    for company_name, job_openings in job_openings_by_company.items():
        company_url = job_openings[0][1]
        body_html += f'<h2><a href="{company_url}" style="color: #{color_scheme["links"]}; text-decoration: none;">{company_name}</a></h2>'
        for job, _ in job_openings:
            body_html += f'<p style="color: #{color_scheme["text"]};">{job}</p>'
        body_html += f'<hr style="border: 0; height: 3px; background-color: #{color_scheme["line"]}; width: 50%; margin: 20px auto;">'

    body_html += f"""
        <hr style="border: 0; height: 5px; background-color: #{color_scheme["line"]}; width: 80%; margin: 20px auto;">
        <h2>Companies that can't be scraped</h2>
    """

    for company_name, company_data in js_companies.items():
        company_url = company_data['url']
        body_html += f'<a href="{company_url}" style="color: #{color_scheme["links"]}; text-decoration: none;">{company_name}</a><br>'

    body_html += f"""
        <hr style="border: 0; height: 5px; background-color: #{color_scheme["line"]}; width: 80%; margin: 20px auto;">
        <h2>Companies to check for open positions</h2>
    """

    for company_name, company_data in no_listing_companies.items():
        company_url = company_data['url']
        body_html += f'<a href="{company_url}" style="color: #{color_scheme["links"]}; text-decoration: none;">{company_name}</a><br>'

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
