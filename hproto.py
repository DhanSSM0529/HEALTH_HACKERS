import wx
import pandas as pd
import hashlib

# Load the dataset and ensure the Contact is treated as a string
df = pd.read_csv('vital_signs.csv', dtype={'Contact': str})
df.columns = df.columns.str.strip().str.lower()

# Sample hashed password for authentication
# In reality, this would be stored securely and checked using a database or a config file
USERNAME = "admin"
PASSWORD_HASH = hashlib.sha256("password".encode()).hexdigest()  # "securepassword" hashed


class LoginDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(LoginDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((300, 200))
        self.SetTitle("Login")

    def InitUI(self):
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        label_font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Username label and input
        username_label = wx.StaticText(panel, label="Username:")
        username_label.SetFont(label_font)
        vbox.Add(username_label, flag=wx.LEFT | wx.TOP, border=10)

        self.username_input = wx.TextCtrl(panel)
        vbox.Add(self.username_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        # Password label and input
        password_label = wx.StaticText(panel, label="Password:")
        password_label.SetFont(label_font)
        vbox.Add(password_label, flag=wx.LEFT | wx.TOP, border=10)

        self.password_input = wx.TextCtrl(panel, style=wx.TE_PASSWORD)  # Password masking
        vbox.Add(self.password_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        # Login button
        login_btn = wx.Button(panel, label="Login")
        login_btn.Bind(wx.EVT_BUTTON, self.OnLogin)
        vbox.Add(login_btn, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        panel.SetSizer(vbox)

    def OnLogin(self, event):
        username = self.username_input.GetValue()
        password = self.password_input.GetValue()

        if self.ValidateCredentials(username, password):
            self.EndModal(wx.ID_OK)  # Close dialog on successful login
        else:
            wx.MessageBox("Invalid username or password.", "Error", wx.OK | wx.ICON_ERROR)

    def ValidateCredentials(self, username, password):
        # Validate username and hashed password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return username == USERNAME and hashed_password == PASSWORD_HASH


class VitalSignsApp(wx.Frame):
    def __init__(self, parent, title):
        super(VitalSignsApp, self).__init__(parent, title=title, size=(400, 500))

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

        # Patient details grid
        grid_sizer = wx.FlexGridSizer(6, 2, 10, 10)
        grid_sizer.AddGrowableCol(1, 1)  # Second column grows

        self.name_label = wx.StaticText(panel, label="Patient Name:")
        self.name_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.name_label, flag=wx.LEFT)
        grid_sizer.Add(self.name_value, flag=wx.EXPAND)

        self.contact_label = wx.StaticText(panel, label="Contact Number:")
        self.contact_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.contact_label, flag=wx.LEFT)
        grid_sizer.Add(self.contact_value, flag=wx.EXPAND)

        self.hr_label = wx.StaticText(panel, label="Heart Rate (bpm):")
        self.hr_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.hr_label, flag=wx.LEFT)
        grid_sizer.Add(self.hr_value, flag=wx.EXPAND)

        self.rr_label = wx.StaticText(panel, label="Respiratory Rate (bpm):")
        self.rr_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.rr_label, flag=wx.LEFT)
        grid_sizer.Add(self.rr_value, flag=wx.EXPAND)

        self.spo2_label = wx.StaticText(panel, label="Oxygen Level (SpO2 %):")
        self.spo2_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.spo2_label, flag=wx.LEFT)
        grid_sizer.Add(self.spo2_value, flag=wx.EXPAND)

        self.temp_label = wx.StaticText(panel, label="Body Temperature (°C):")
        self.temp_value = wx.StaticText(panel, label="N/A")
        grid_sizer.Add(self.temp_label, flag=wx.LEFT)
        grid_sizer.Add(self.temp_value, flag=wx.EXPAND)

        vbox.Add(grid_sizer, flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)

        # Result message
        self.result_label = wx.StaticText(panel, label="Status: ")
        self.result_label.SetFont(label_font)
        vbox.Add(self.result_label, flag=wx.LEFT | wx.TOP, border=10)

        # Add Remedy Button (initially hidden)
        self.remedy_button = wx.Button(panel, label="Get Remedy")
        self.remedy_button.SetFont(input_font)
        self.remedy_button.SetBackgroundColour(wx.Colour(40, 167, 69))
        self.remedy_button.SetForegroundColour(wx.Colour(255, 255, 255))
        self.remedy_button.Bind(wx.EVT_BUTTON, self.get_remedy)
        self.remedy_button.Hide()  # Hide initially
        vbox.Add(self.remedy_button, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def search_patient(self, event):
        name = self.search_input.GetValue().strip()
        patient_data = df[df['name'].str.lower() == name.lower()]

        if not patient_data.empty:
            patient = patient_data.iloc[0]
            self.name_value.SetLabel(f"{patient['name']}")
            self.contact_value.SetLabel(f"{patient['contact']}")
            self.hr_value.SetLabel(f"{patient['heartrate']}")
            self.rr_value.SetLabel(f"{patient['resprate']}")
            self.spo2_value.SetLabel(f"{patient['spo2']}")
            self.temp_value.SetLabel(f"{patient['temperature']}")

            if (60 <= patient['heartrate'] <= 100 and
                12 <= patient['resprate'] <= 18 and
                95 <= patient['spo2'] <= 100 and
                36.5 <= patient['temperature'] <= 37.5):
                self.result_label.SetLabel("Status: Normal")
                self.result_label.SetForegroundColour(wx.Colour(0, 128, 0))
                self.remedy_button.Hide()  # Hide remedy button for normal vitals
            else:
                self.result_label.SetLabel("Status: Abnormal")
                self.result_label.SetForegroundColour(wx.Colour(255, 0, 0))
                self.remedy_button.Show()  # Show remedy button for abnormal vitals
        else:
            wx.MessageBox("Patient not found!", "Error", wx.OK | wx.ICON_ERROR)

    def get_remedy(self, event):
        remedy = self.fetch_remedy_from_api()
        wx.MessageBox(f"Suggested Remedy:\n\n{remedy}", "Remedy", wx.OK | wx.ICON_INFORMATION)

    def fetch_remedy_from_api(self):
        return "For abnormal heart rate, maintain hydration and reduce stress.\nFor abnormal SpO2, try deep breathing exercises."

if __name__ == '__main__':
    app = wx.App()

    login = LoginDialog(None)
    if login.ShowModal() == wx.ID_OK:  # Show login dialog
        frame = VitalSignsApp(None, title="Vital Signs Anomaly Detection")
        app.MainLoop()
    else:
        wx.MessageBox("Login failed. Exiting application.", "Error", wx.OK | wx.ICON_ERROR)
        app.Exit()
