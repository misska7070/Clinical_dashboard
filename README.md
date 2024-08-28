# Clinical Analytics Dashboard

This repository contains an interactive clinical analytics dashboard designed to help clinical teams review performance and identify trends to optimise patient care and resource allocation.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Data Files](#data-files)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)

## Introduction

The Clinical Analytics Dashboard provides visual insights into patient response times, team performance, and trends over time. The dashboard is built using Python, Dash, and Plotly and offers various interactive visualisations to assist clinicians in planning their capacity and improving patient care.

## Features

- **Interactive Visualisations**: Line charts, scatter plots, and heatmaps to analyse response times and team overlaps.
- **Dynamic Filtering**: Ability to filter by organisation, team, and date range for tailored insights.
- **Trend Analysis**: Visualise trends in response times across different time frames (year, month, week).

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/clinical-analytics-dashboard.git
    cd clinical-analytics-dashboard
    ```

2. **Set up a virtual environment (recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Dashboard**:

    Ensure you are in the root directory of the project where `dashboard_tabs.py` is located.

    ```bash
    python dashboard_tabs.py
    ```

2. **Open the Dashboard**:

    After running the script, open a web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

3. **Adjust File Paths (if necessary)**:

   If you encounter any `FileNotFoundError`, ensure that the Excel files (`cleaned_response_output.xlsx` and `no_response_output.xlsx`) are in the same directory as `dashboard_tabs.py`. If they are located elsewhere, adjust the paths in the script accordingly:

    ```python
    cleaned_response_times_df = pd.read_excel('path/to/cleaned_response_output.xlsx')
    no_responses_df = pd.read_excel('path/to/no_response_output.xlsx')
    ```

## Data Files

This project relies on the following Excel files:

- **cleaned_response_output.xlsx**: Contains the cleaned and processed data on patient entries and corresponding clinician actions.
- **no_response_output.xlsx**: Contains data on patient entries that did not receive any clinician response.

### Data Structure

- **cleaned_response_output.xlsx**: Includes columns like `collectionId`, `entry_date`, `earliest_entry_time`, `closest_response_time`, `response_time_hours`, `userId`, `patientId`, `teamId`, `organisationId`, and calculated metrics like `mean_response_time`, `std_response_time`, `z_score`, `weight`, and `weighted_response_time`.

- **no_response_output.xlsx**: Focuses on entries that lack a corresponding action from clinicians, highlighting potential gaps in patient care.

## Future Enhancements

The following enhancements are planned for future releases:

- **Calendar Date Range Filter**: Add a more interactive date selection tool allowing users to filter data by custom date ranges.
- **Advanced Analytics**: Introduce predictive analytics to forecast future trends in response times and patient care needs.
- **Real-time Data Integration**: Implement real-time data updates to provide clinicians with the most current information possible.
- **User Authentication**: Introduce user authentication and role-based access to ensure data security and privacy.

## Edge Cases

During the development, the following edge cases were considered:

1. **Leap Year Handling**: Incorrect dates like 29th February 2014 were identified and removed as 2014 was not a leap year.
2. **Ghost Entries**: Instances where clinician actions had no corresponding patient entries were flagged and handled to prevent erroneous analysis.
3. **Data Gaps**: Entries without corresponding clinician actions (indicating no response) were analysed separately to understand gaps in patient care.

## Contact

For any questions or issues, please reach out to the project maintainer:

- **Name**: Khadija Anam
- **Email**: khadijaanam.work@gmail.com
- **GitHub**: https://github.com/misska7070

---

Thank you for using the Clinical Analytics Dashboard! We hope it helps improve patient care and streamline your clinical processes.
