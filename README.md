# Loan Application Evaluation System

This is a Streamlit-based web application that evaluates loan applications using an expert system built with Experta. The system determines whether a loan should be approved or denied based on various applicant details.

## Features
- User-friendly Streamlit interface for inputting loan application details.
- Expert system rules implemented using Experta to evaluate applications.
- Instant feedback on loan approval decision.
- Displays approved loan amount if eligible.

## Installation

### Prerequisites
Make sure you have Python installed on your system. Then, install the required dependencies:

```sh
pip install -r requirements.txt
```

**Note:** To avoid compatibility issues, such as errors related to `collections.Mapping` in Python 3.10+, ensure that `frozendict==2.3.8` is installed:
```sh
pip install frozendict==2.3.8
```

### Virtual Environment Setup (Recommended)
To prevent dependency conflicts, create a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
pip install -r requirements.txt
```

## Usage
To run the application, execute the following command:

```sh
streamlit run main.py
```

## Application Logic
The system evaluates loan applications based on various factors, including:
- Age
- Marital status
- Employment status
- Annual income
- Family size
- Loan amount requested
- Existing debt
- Loan purpose
- Loan term
- Monthly expenses
- Collateral availability
- Bankruptcy history

The expert system applies specific rules to determine whether the loan is approved or denied. If approved, the maximum loan amount is calculated based on the applicant's income.

## Hosted Application
You can access the live application here: [Loan Approval Expert System](https://loan-approval-expert-system.streamlit.app/)

## Files in this Repository
- `.streamlit/` - Contains the Streamlit configuration files.
- `main.py` - The main application file containing the expert system and Streamlit UI.
- `requirements.txt` - List of required dependencies.
- `.gitignore` - Git ignore file to exclude unnecessary files from version control.


## Authors
Developed by: 
- Denis Kimathi Mugambi 
- Brian Gatoto
- Joe Kuya
- Billy Kiplangat Ngetich
- Omondi Isaac Odhiambo
- Calvin Kirui
- Caltone Smith
- Kiptoo Ian

## License
This project is licensed under the MIT License.