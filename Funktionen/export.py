from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os
import pandas as pd
import logging

# Directories for CSV and PDF
csv_dir = 'KMM_Abschlussprojekt_Programmieruebung2/CSV'
pdf_dir = 'KMM_Abschlussprojekt_Programmieruebung2/PDF'
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)


def filter_dataframe(df, start_date, end_date):
    """Filters the DataFrame based on the selected date range.

    Args:
        df (pandas.DataFrame): The DataFrame to be filtered.
        start_date (str): The start date of the date range.
        end_date (str): The end date of the date range.

    Returns:
        pandas.DataFrame: The filtered DataFrame.
    """
    df['activity_date'] = pd.to_datetime(df['activity_date']).dt.date
    return df[(df['activity_date'] >= start_date) & (df['activity_date'] <= end_date)]


def export_to_csv(df_selected):
    """Exports the DataFrame as a CSV file.

    Args:
        df_selected (pandas.DataFrame): The DataFrame to be exported.

    Returns:
        str: The path of the exported CSV file.
    Raises:
        Exception: If an error occurs during the export process.
    """
    try:
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = os.path.join(csv_dir, f"{time}_overview_data.csv")
        df_selected.to_csv(csv_path, index=False)
        return csv_path
    except Exception as e:
        logging.exception('Error exporting as CSV!')
        raise e


def export_to_pdf(df_selected, df_summary_selected):
    """Exports the DataFrame as a PDF file.

    Args:
        df_selected (pandas.DataFrame): The DataFrame to be exported.
        df_summary_selected (pandas.DataFrame): The summary DataFrame to be exported.

    Returns:
        str: The path of the exported PDF file.
    Raises:
        Exception: If an error occurs during the export process.
    """
    try:
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_pdf_path = os.path.join(pdf_dir, f"{time}_overview_data.pdf")
        pdf = SimpleDocTemplate(output_pdf_path, pagesize=landscape(letter))

        # Convert the DataFrame to a list of lists for the Table
        data = [df_selected.columns.tolist()] + df_selected.values.tolist()
        data1 = [df_summary_selected.columns.tolist()] + df_summary_selected.values.tolist()
        table = Table(data)
        table1 = Table(data1)

        # Define the style of the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(table_style)
        table1.setStyle(table_style)

        # Include the tables in the PDF
        elements = [table, table1]

        pdf.build(elements)
        return output_pdf_path
    except Exception as e:
        logging.exception('Error exporting as PDF!')
        raise e
