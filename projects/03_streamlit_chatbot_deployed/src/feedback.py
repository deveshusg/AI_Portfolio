# ==================================================
# IMPORTS
# ==================================================
#
# datetime
# --------------------------------------------------
# Used to timestamp feedback submissions.
#
# gspread
# --------------------------------------------------
# Python client for Google Sheets.
#
# streamlit
# --------------------------------------------------
# Accesses Streamlit Cloud secrets.
#
# google.oauth2.service_account
# --------------------------------------------------
# Authenticates using a Google Service Account.
#
# ==================================================

from datetime import datetime

import gspread
import streamlit as st

from google.oauth2.service_account import (
    Credentials
)

# ==================================================
# GOOGLE API SCOPES
# ==================================================
#
# Purpose
# --------------------------------------------------
# Defines what permissions the service account
# has when connecting to Google services.
#
# spreadsheets
#     Read/write spreadsheet data.
#
# drive
#     Access spreadsheet files stored in Drive.
#
# ==================================================

SCOPES = [

    "https://www.googleapis.com/auth/spreadsheets",

    "https://www.googleapis.com/auth/drive",
]

# ==================================================
# FEEDBACK SPREADSHEET
# ==================================================
#
# Purpose
# --------------------------------------------------
# Google Sheet used to store feedback.
#
# Current Sheet:
# --------------------------------------------------
# AI Chatbot Feedback
#
# ==================================================

SPREADSHEET_ID = (
    "1D1nw3Uk0QJ8aUmpS8oxL86FHzQSAa0xp5-DgZmWA2GQ"
)

# ==================================================
# GOOGLE SHEETS CONNECTION
# ==================================================
#
# Purpose
# --------------------------------------------------
# Creates an authenticated connection to
# Google Sheets.
#
# Process
# --------------------------------------------------
# 1. Read credentials from Streamlit secrets.
# 2. Create service account credentials.
# 3. Authorize gspread.
# 4. Open feedback spreadsheet.
# 5. Return first worksheet.
#
# ==================================================

def get_sheet():

    if (
        "gcp_service_account"
        not in st.secrets
    ):

        raise Exception(
            (
                "Google Sheets credentials "
                "are not configured."
            )
        )

    credentials = (
        Credentials
        .from_service_account_info(
            dict(
                st.secrets[
                    "gcp_service_account"
                ]
            ),
            scopes=SCOPES,
        )
    )

    client = gspread.authorize(
        credentials
    )

    spreadsheet = (
        client.open_by_key(
            SPREADSHEET_ID
        )
    )

    return spreadsheet.sheet1

# ==================================================
# SAVE FEEDBACK
# ==================================================
#
# Purpose
# --------------------------------------------------
# Saves a feedback record into Google Sheets.
#
# Stored Columns
# --------------------------------------------------
# Timestamp
# Name
# Email
# Feedback
# Chat ID
# Chat Log
#
# Notes
# --------------------------------------------------
# Chat Log contains the most recent messages
# from the conversation and is useful for:
#
# - Bug investigations
# - Prompt improvement
# - User experience analysis
#
# ==================================================

def save_feedback(
    name,
    email,
    feedback,
    chat_id,
    chat_log,
):

    sheet = get_sheet()

    timestamp = (
        datetime.utcnow()
        .strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    row = [

        timestamp,

        name,

        email,

        feedback,

        chat_id,

        chat_log,
    ]

    sheet.append_row(
        row
    )