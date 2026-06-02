from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SPREADSHEET_ID = "1D1nw3Uk0QJ8aUmpS8oxL86FHzQSAa0xp5-DgZmWA2GQ"


def get_sheet():
    
    if "gcp_service_account" not in st.secrets:
        raise Exception(
        "Google Sheets secrets not configured."
    )

    credentials = Credentials.from_service_account_info(
        dict(st.secrets["gcp_service_account"]),
        scopes=SCOPES,
    )

    client = gspread.authorize(credentials)

    return client.open_by_key(SPREADSHEET_ID).sheet1


def save_feedback(
    name,
    email,
    feedback,
    chat_id,
    chat_log,
):

    sheet = get_sheet()

    timestamp = datetime.utcnow().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    sheet.append_row(
        [
            timestamp,
            name,
            email,
            feedback,
            chat_id,
            chat_log,
        ]
    )