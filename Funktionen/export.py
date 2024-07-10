# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
# from reportlab.lib import colors
# from reportlab.lib.styles import getSampleStyleSheet
# import logging
# import os

# # Stellen Sie sicher, dass die Verzeichnisse existieren oder erstellen Sie sie
# csv_dir = 'KMM_Abschlussprojekt_Programmieruebung2/CSV'
# pdf_dir = 'KMM_Abschlussprojekt_Programmieruebung2/PDF'
# os.makedirs(csv_dir, exist_ok=True)
# os.makedirs(pdf_dir, exist_ok=True)


# if isinstance(selected_date, tuple):
#     start_date = selected_date[0]  # Umwandlung in datetime.date
#     end_date = selected_date[1]  # Umwandlung in datetime.date

#     # Sicherstellen, dass activity_date im datetime.date-Format ist
#     df_overview['activity_date'] = pd.to_datetime(df_overview['activity_date']).dt.date
    
#     # Filtern der Datenframes nach dem ausgewählten Datumbereich
#     df_selected = df_overview[(df_overview['activity_date'] >= start_date) & 
#                             (df_overview['activity_date'] <= end_date)]


#     # Export-Buttons und Logik
#     try:
#         if st.button("Export all to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):
#             time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             csv_path = os.path.join(csv_dir, f"{time}_overview_data.csv")
#             df_selected.to_csv(csv_path, index=False)
#             st.success(f"Data successfully exported to {csv_path}")

#             # Seite neu laden
#             st.experimental_rerun()
#     except Exception as e:
#         logging.exception('Fehler beim Exportieren als CSV!')
#         st.write(f"Fehler beim Exportieren als CSV! {e}")

#     try:
#         if st.button("Export all to PDF", help="Klicken Sie hier um die Daten als PDF zu exportieren!"):
#             time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             output_pdf_path = os.path.join(pdf_dir, f"{time}_overview_data.pdf")
#             pdf = SimpleDocTemplate(output_pdf_path, pagesize=letter)

#             # Convert the DataFrame to a list of lists for the Table
#             data = [df_selected.columns.tolist()] + df_selected.values.tolist()
#             table = Table(data)

#             # Define the style of the table
#             table_style = TableStyle([
#                 ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                 ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ])

#             table.setStyle(table_style)

#             # Include the table in the PDF
#             elements = [table]

#             pdf.build(elements)
#             st.success(f"Data successfully exported to {output_pdf_path}")
#     except Exception as e:
#         logging.exception('Fehler beim Exportieren als PDF!')
#         st.write(f"Fehler beim Exportieren als PDF! {e}")

# else:
#     st.write("Bitte wählen Sie einen gültigen Zeitraum aus.")
