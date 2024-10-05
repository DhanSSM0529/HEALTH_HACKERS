import wx
import pandas as pd

# Load the dataset and ensure the Contact is treated as a string
df = pd.read_csv('vital_signs.csv', dtype={'Contact': str})
df.columns = df.columns.str.strip().str.lower()

# Print columns for debugging (optional)
print("Columns in dataset:", df.columns)

class VitalSignsApp(wx.Frame):
    def __init__(self, parent, title):
        super(VitalSignsApp, self).__init__(parent, title=title, size=(400, 450))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Set background color for the panel
        panel.SetBackgroundColour('#e9ecef')

        # Define custom fonts for labels and buttons
        label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        # Title
        title_label = wx.StaticText(panel, label="Vital Signs Anomaly Detection")
        title_label.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title_label.SetForegroundColour(wx.Colour(0, 51, 102))
        vbox.Add(title_label, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        # Search for patient
        self.search_label = wx.StaticText(panel, label="Search Patient by Name:")
        self.search_label.SetFont(label_font)
        vbox.Add(self.search_label, flag=wx.LEFT | wx.TOP, border=10)

        self.search_input = wx.TextCtrl(panel)
        self.search_input.SetFont(input_font)
        vbox.Add(self.search_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        # Add Search Button
        self.search_button = wx.Button(panel, label="Search")
        self.search_button.SetFont(input_font)
        self.search_button.SetBackgroundColour(wx.Colour(0, 123, 255))
        self.search_button.SetForegroundColour(wx.Colour(255, 255, 255))
        self.search_button.Bind(wx.EVT_BUTTON, self.search_patient)
        vbox.Add(self.search_button, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        # Patient information fields
        self.name_label = wx.StaticText(panel, label="Patient Name:")
        self.name_label.SetFont(label_font)
        vbox.Add(self.name_label, flag=wx.LEFT | wx.TOP, border=10)

        self.contact_label = wx.StaticText(panel, label="Contact Number:")
        self.contact_label.SetFont(label_font)
        vbox.Add(self.contact_label, flag=wx.LEFT | wx.TOP, border=10)

        self.hr_label = wx.StaticText(panel, label="Heart Rate (bpm):")
        self.hr_label.SetFont(label_font)
        vbox.Add(self.hr_label, flag=wx.LEFT | wx.TOP, border=10)

        self.rr_label = wx.StaticText(panel, label="Respiratory Rate (bpm):")
        self.rr_label.SetFont(label_font)
        vbox.Add(self.rr_label, flag=wx.LEFT | wx.TOP, border=10)

        self.spo2_label = wx.StaticText(panel, label="Oxygen Level (SpO2 %):")
        self.spo2_label.SetFont(label_font)
        vbox.Add(self.spo2_label, flag=wx.LEFT | wx.TOP, border=10)

        self.temp_label = wx.StaticText(panel, label="Body Temperature (°C):")
        self.temp_label.SetFont(label_font)
        vbox.Add(self.temp_label, flag=wx.LEFT | wx.TOP, border=10)

        # Result message
        self.result_label = wx.StaticText(panel, label="Status: ")
        self.result_label.SetFont(label_font)
        vbox.Add(self.result_label, flag=wx.LEFT | wx.TOP, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def search_patient(self, event):
        name = self.search_input.GetValue().strip()
        # Search for the patient in the dataset (case-insensitive)
        patient_data = df[df['name'].str.lower() == name.lower()]

        if not patient_data.empty:
            # Display patient details
            patient = patient_data.iloc[0]
            self.name_label.SetLabel(f"Patient Name: {patient['name']}")
            self.contact_label.SetLabel(f"Contact Number: {patient['contact']}")
            self.hr_label.SetLabel(f"Heart Rate (bpm): {patient['heartrate']}")
            self.rr_label.SetLabel(f"Respiratory Rate (bpm): {patient['resprate']}")
            self.spo2_label.SetLabel(f"Oxygen Level (SpO2 %): {patient['spo2']}")
            self.temp_label.SetLabel(f"Body Temperature (°C): {patient['temperature']}")

            # Determine if vital signs are within normal ranges
            if (60 <= patient['heartrate'] <= 100 and
                12 <= patient['resprate'] <= 18 and
                95 <= patient['spo2'] <= 100 and
                36.5 <= patient['temperature'] <= 37.5):
                self.result_label.SetLabel("Status: Normal")
                self.result_label.SetForegroundColour(wx.Colour(0, 128, 0))  # Green for normal
            else:
                self.result_label.SetLabel("Status: Abnormal")
                self.result_label.SetForegroundColour(wx.Colour(255, 0, 0))  # Red for abnormal
        else:
            wx.MessageBox("Patient not found!", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == '__main__':
    app = wx.App()
    frame = VitalSignsApp(None, title="Vital Signs Anomaly Detection with Dataset")
    app.MainLoop()
