import wx

class VitalSignsApp(wx.Frame):
    def __init__(self, parent, title):
        super(VitalSignsApp, self).__init__(parent, title=title, size=(400, 400))
        
        # Panel for the input fields and labels
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Set background color for the panel
        panel.SetBackgroundColour('#f2f2f2')

        # Define custom font for labels
        label_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        input_font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        # Name input
        self.name_label = wx.StaticText(panel, label="Patient Name:")
        self.name_label.SetFont(label_font)
        self.name_label.SetForegroundColour(wx.Colour(0, 0, 128))  # Dark Blue Text
        vbox.Add(self.name_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.name_input = wx.TextCtrl(panel)
        self.name_input.SetFont(input_font)
        vbox.Add(self.name_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Contact input
        self.contact_label = wx.StaticText(panel, label="Contact Number:")
        self.contact_label.SetFont(label_font)
        self.contact_label.SetForegroundColour(wx.Colour(0, 0, 128))
        vbox.Add(self.contact_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.contact_input = wx.TextCtrl(panel)
        self.contact_input.SetFont(input_font)
        vbox.Add(self.contact_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Heart Rate input
        self.hr_label = wx.StaticText(panel, label="Heart Rate (bpm):")
        self.hr_label.SetFont(label_font)
        self.hr_label.SetForegroundColour(wx.Colour(0, 0, 128))
        vbox.Add(self.hr_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.hr_input = wx.TextCtrl(panel)
        self.hr_input.SetFont(input_font)
        vbox.Add(self.hr_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Respiratory Rate input
        self.rr_label = wx.StaticText(panel, label="Respiratory Rate (bpm):")
        self.rr_label.SetFont(label_font)
        self.rr_label.SetForegroundColour(wx.Colour(0, 0, 128))
        vbox.Add(self.rr_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.rr_input = wx.TextCtrl(panel)
        self.rr_input.SetFont(input_font)
        vbox.Add(self.rr_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Oxygen level input
        self.spo2_label = wx.StaticText(panel, label="Oxygen Level (SpO2 %):")
        self.spo2_label.SetFont(label_font)
        self.spo2_label.SetForegroundColour(wx.Colour(0, 0, 128))
        vbox.Add(self.spo2_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.spo2_input = wx.TextCtrl(panel)
        self.spo2_input.SetFont(input_font)
        vbox.Add(self.spo2_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Body temperature input
        self.temp_label = wx.StaticText(panel, label="Body Temperature (°C):")
        self.temp_label.SetFont(label_font)
        self.temp_label.SetForegroundColour(wx.Colour(0, 0, 128))
        vbox.Add(self.temp_label, flag=wx.LEFT | wx.TOP, border=10)
        
        self.temp_input = wx.TextCtrl(panel)
        self.temp_input.SetFont(input_font)
        vbox.Add(self.temp_input, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        
        # Submit button with style
        self.submit_button = wx.Button(panel, label="Check Vitals")
        self.submit_button.SetBackgroundColour(wx.Colour(0, 128, 0))  # Green button
        self.submit_button.SetForegroundColour(wx.Colour(255, 255, 255))  # White text
        self.submit_button.SetFont(label_font)
        vbox.Add(self.submit_button, flag=wx.LEFT | wx.TOP | wx.EXPAND, border=10)
        self.submit_button.Bind(wx.EVT_BUTTON, self.check_vitals)
        
        # Result message
        self.result = wx.StaticText(panel, label="")
        self.result.SetFont(label_font)
        self.result.SetForegroundColour(wx.Colour(255, 0, 0))  # Red color for result
        vbox.Add(self.result, flag=wx.LEFT | wx.TOP, border=10)
        
        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def check_vitals(self, event):
        # Get values from the input fields
        name = self.name_input.GetValue()
        contact = self.contact_input.GetValue()
        heart_rate = int(self.hr_input.GetValue())
        resp_rate = int(self.rr_input.GetValue())
        spo2 = int(self.spo2_input.GetValue())
        temp = float(self.temp_input.GetValue())
        
        # Check normality of each vital sign
        hr_normal = 60 <= heart_rate <= 100
        rr_normal = 12 <= resp_rate <= 18
        spo2_normal = 95 <= spo2 <= 100
        temp_normal = 36.5 <= temp <= 37.5
        
        # Generate result message
        message = f"Patient: {name}\nContact: {contact}\n\n"
        if hr_normal and rr_normal and spo2_normal and temp_normal:
            message += "All vitals are normal."
            self.result.SetForegroundColour(wx.Colour(0, 128, 0))  # Green color for normal result
        else:
            message += "Abnormal vitals detected:\n"
            if not hr_normal:
                message += "- Heart Rate abnormal\n"
            if not rr_normal:
                message += "- Respiratory Rate abnormal\n"
            if not spo2_normal:
                message += "- Oxygen Level abnormal\n"
            if not temp_normal:
                message += "- Body Temperature abnormal\n"
            self.result.SetForegroundColour(wx.Colour(255, 0, 0))  # Red color for abnormal result
        
        self.result.SetLabel(message)

if __name__ == '__main__':
    app = wx.App()
    frame = VitalSignsApp(None, title="Vital Signs Anomaly Detection")
    app.MainLoop()
