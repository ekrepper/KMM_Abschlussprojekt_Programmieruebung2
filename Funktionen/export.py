from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os
import pandas as pd
import logging

# Verzeichnisse für CSV und PDF
csv_dir = 'KMM_Abschlussprojekt_Programmieruebung2/CSV'
pdf_dir = 'KMM_Abschlussprojekt_Programmieruebung2/PDF'
os.makedirs(csv_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)


def filter_dataframe(df, start_date, end_date):
    """ Filtert das DataFrame nach dem ausgewählten Datumbereich. """
    df['activity_date'] = pd.to_datetime(df['activity_date']).dt.date
    return df[(df['activity_date'] >= start_date) & (df['activity_date'] <= end_date)]


def export_to_csv(df_selected):
    """ Exportiert das DataFrame als CSV. """
    try:
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_path = os.path.join(csv_dir, f"{time}_overview_data.csv")
        df_selected.to_csv(csv_path, index=False)
        return csv_path
    except Exception as e:
        logging.exception('Fehler beim Exportieren als CSV!')
        raise e


def export_to_pdf(df_selected):
    """ Exportiert das DataFrame als PDF. """
    try:
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_pdf_path = os.path.join(pdf_dir, f"{time}_overview_data.pdf")
        pdf = SimpleDocTemplate(output_pdf_path, pagesize=landscape(letter))

        # Convert the DataFrame to a list of lists for the Table
        data = [df_selected.columns.tolist()] + df_selected.values.tolist()
        table = Table(data)

        # Define the style of the table
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        table.setStyle(table_style)

        # Include the table in the PDF
        elements = [table]

        pdf.build(elements)
        return output_pdf_path
    except Exception as e:
        logging.exception('Fehler beim Exportieren als PDF!')
        raise e
