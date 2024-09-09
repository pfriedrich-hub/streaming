import openpyxl
# Excel Python Paket importieren

def aktualisiere_excel(Versuche, workbook, Kind_Nr_x):
    sheet = workbook.active
    Zeilensprung_plus = 0
    for Versuch in Versuche:
        responses_52_5 = Versuch[0]
        responses_35 = Versuch[1]
        responses_17_5 = Versuch[2]

        sheet[f"B{2 + Zeilensprung_plus}"].value = responses_52_5[0]
        sheet[f"B{3 + Zeilensprung_plus}"].value = responses_52_5[1]
        sheet[f"B{4 + Zeilensprung_plus}"].value = responses_52_5[2]
        sheet[f"B{5 + Zeilensprung_plus}"].value = responses_52_5[0] + responses_52_5[1] + responses_52_5[2]

        sheet[f"C{2 + Zeilensprung_plus}"].value = responses_35[0]
        sheet[f"C{3 + Zeilensprung_plus}"].value = responses_35[1]
        sheet[f"C{4 + Zeilensprung_plus}"].value = responses_35[2]
        sheet[f"C{5 + Zeilensprung_plus}"].value = responses_35[0] + responses_35[1] + responses_35[2]

        sheet[f"D{2 + Zeilensprung_plus}"].value = responses_17_5[0]
        sheet[f"D{3 + Zeilensprung_plus}"].value = responses_17_5[1]
        sheet[f"D{4 + Zeilensprung_plus}"].value = responses_17_5[2]
        sheet[f"D{5 + Zeilensprung_plus}"].value = responses_17_5[0] + responses_17_5[1] + responses_17_5[2]

        # Einfügen der Antworten in Excel

        sheet[f"A{1 + Zeilensprung_plus}"].value = "Subject-ID"
        sheet[f"B{2 + Zeilensprung_plus}"].value = "masker 52.5°"
        sheet[f"C{1 + Zeilensprung_plus}"].value = "masker 35°"
        sheet[f"D{1 + Zeilensprung_plus}"].value = "masker 17.5°"
        sheet[f"A{2 + Zeilensprung_plus}"].value = "hits"
        sheet[f"A{3 + Zeilensprung_plus}"].value = "missed"
        sheet[f"A{4 + Zeilensprung_plus}"].value = "false positive"
        sheet[f"A{5 + Zeilensprung_plus}"].value = "Summe"

        Zeilensprung_plus =  Zeilensprung_plus + 7

    # Spalten - & Zeilenbenennung in Excel

    workbook.save('Streaming_noise_neu.xlsx')

workbook_Kind_x = openpyxl.Workbook()

Versuche = []
Versuch_1 = []
responses_Kind_x_52_5 = [8, 10, 5]
responses_Kind_x_35 = [6, 8, 7]
responses_Kind_x_17_5 = [4, 5, 7]
Versuch_1.append(responses_Kind_x_52_5)
Versuch_1.append(responses_Kind_x_35)
Versuch_1.append(responses_Kind_x_17_5)
Versuche.append(Versuch_1)

#Kopiere diesen Block und ändere die Nummer des Versuchs für nächste Kind, um einen neuen Block zu bekommen. Die blauen Zahlen sind nur exemplarisch für die Antworten des Knopfdrucks

#Versuch_2 = []
#responses_Kind_x_52_5 = [8, 10, 5]
#responses_Kind_x_35 = [6, 8, 7]
#responses_Kind_x_17_5 = [4, 5, 7]
#Versuch_2.append(responses_Kind_x_52_5)
#Versuch_2.append(responses_Kind_x_35)
#Versuch_2.append(responses_Kind_x_17_5)
#Versuche.append(Versuch_2)


Kind_Nr_x = 0
# Nummer des getesteten Kindes, muss immer geändert werden!!!
aktualisiere_excel(Versuche, workbook_Kind_x, Kind_Nr_x)


