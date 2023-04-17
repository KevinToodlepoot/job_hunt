import parse_functions

# define companies dictionary
companies = {
    'Eventide': {
        'url': 'https://www.eventideaudio.com/employment',
        'parse_function': parse_functions.eventide,
    },
    'Sonible': {
        'url': 'https://www.sonible.com/jobs/',
        'parse_function': parse_functions.sonible,
    },
    'Universal Audio': {
        'url': 'https://boards.greenhouse.io/universalaudio',
        'parse_function': parse_functions.greenhouse,
    },
    'Output': {
        'url': 'https://boards.greenhouse.io/output',
        'parse_function': parse_functions.greenhouse,
    },
    'Spectrasonics': {
        'url': 'https://www.spectrasonics.net/company/employment.php',
        'parse_function': parse_functions.spectrasonics,
    },
    'Izotope': {
        'url': 'https://boards.greenhouse.io/izotopecareers',
        'parse_function': parse_functions.greenhouse,
    },
    'Sonnox': {
        'url': 'https://www.sonnox.com/about/jobs',
        'parse_function': parse_functions.sonnox,
    },
    'Soundtoys': {
        'url': 'https://www.soundtoys.com/jobs/',
        'parse_function': parse_functions.soundtoys,
    },
    'Apogee': {
        'url': 'https://apogeedigital.com/company/job',
        'parse_function': parse_functions.apogee,
    },
    'Ableton': {
        'url': 'https://www.ableton.com/en/jobs/',
        'parse_function': parse_functions.ableton,
    },
    'MOTU': {
        'url': 'https://motu.com/en-us/company/careers/',
        'parse_function': parse_functions.motu,
    },
    'Reason': {
        'url': 'https://careers.reasonstudios.com/#jobs',
        'parse_function': parse_functions.reason_xln,
    },
    'XLN Audio': {
        'url': 'https://careers.xlnaudio.com/#jobs',
        'parse_function': parse_functions.reason_xln,
    },
}

js_companies = {
    'Arturia': {
        'url': 'https://jobs.arturia.com/',
    },
    'Native Instruments': {
        'url': 'https://www.native-instruments.com/en/career-center',
    },
    'Softube': {
        'url': 'https://softube.bamboohr.com/jobs/',
    },
    'SSL': {
        'url': 'https://www.solidstatelogic.com/careers',
    },
    'Sound Particles': {
        'url': 'https://soundparticles.com/careers',
    },
    'Focusrite': {
        'url': 'https://apply.workable.com/focusrite/#jobs',
    },
    'Slate Digital': {
        'url': 'https://slatedigital.com/careers/',
    },
    'Presonus': {
        'url': 'https://www.fender.com/pages/careers',
    },
}

no_listing_companies = {
    'Waves': {
        'url': 'https://www.waves.com/careers',
    },
    'Roland': {
        'url': 'https://www.roland.com/us/company/employment_opportunities/',
    },
    'Serato': {
        'url': 'https://serato.com/careers',
    },
}