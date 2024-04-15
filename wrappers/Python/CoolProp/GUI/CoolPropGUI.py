import wx
import wx.grid
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as WXCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as WXToolbar
import matplotlib as mpl
import CoolProp as CP
from CoolProp.Plots.Plots import Ph, Ts
from CoolProp.Plots import PsychChart
import numpy as np


# Munge the system path if necessary to add the lib folder (only really needed
# for packaging using cx_Freeze)
# if os.path.exists('lib') and os.path.abspath(os.path.join(os.curdir,'lib')) not in os.:


class PlotPanel(wx.Panel):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.figure = mpl.figure.Figure(dpi=100)
        self.canvas = WXCanvas(self, -1, self.figure)
        self.ax = self.figure.add_axes((0.15, 0.15, 0.8, 0.8))
        # self.toolbar = WXToolbar(self.canvas)
        # self.toolbar.Realize()
        sizer.Add(self.canvas, 1, wx.EXPAND)
        # sizer.Add(self.toolbar)
        self.SetSizer(sizer)
        sizer.Layout()


class TSPlotFrame(wx.Frame):
    def __init__(self, Fluid):
        wx.Frame.__init__(self, None, title='T-s plot: ' + Fluid)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.PP = PlotPanel(self, size=(-1, -1))

        sizer.Add(self.PP, 1, wx.EXPAND)
        self.SetSizer(sizer)
        Ts(str(Fluid),
           axis=self.PP.ax,
           Tmin=CP.CoolProp.Props(str(Fluid), 'Ttriple') + 0.01)
        sizer.Layout()

        self.MenuBar = None
        self.File = None
        self.add_menu()

    def add_menu(self):
        # Menu Bar
        self.MenuBar = wx.MenuBar()
        self.File = wx.Menu()

        mnu_item = wx.MenuItem(self.File, -1, "Edit...", "", wx.ITEM_NORMAL)

        self.File.AppendItem(mnu_item)
        self.MenuBar.Append(self.File, "File")

        self.SetMenuBar(self.MenuBar)


class PsychOptions(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.p_label = None
        self.p = None
        self.Tmin_label = None
        self.Tmin = None
        self.Tmax_label = None
        self.Tmax = None
        self.GoButton = None

        self.build_contents()
        self.layout()

    def build_contents(self):
        self.p_label = wx.StaticText(self, label='Pressure [kPa (absolute)]')
        self.p = wx.TextCtrl(self, value='101.325')
        self.Tmin_label = wx.StaticText(self, label='Minimum dry bulb temperature [\xb0 C]')
        self.Tmin = wx.TextCtrl(self, value='-10')
        self.Tmax_label = wx.StaticText(self, label='Maximum dry bulb temperature [\xb0 C]')
        self.Tmax = wx.TextCtrl(self, value='60')
        self.GoButton = wx.Button(self, label='Accept')
        self.GoButton.Bind(wx.EVT_BUTTON, self.OnAccept)

    def OnAccept(self, event):
        self.EndModal(wx.ID_OK)

    def layout(self):
        sizer = wx.FlexGridSizer(cols=2)
        sizer.AddMany([self.p_label, self.p, self.Tmin_label, self.Tmin, self.Tmax_label, self.Tmax])
        sizer.Add(self.GoButton)
        sizer.Layout()
        self.Fit()


class PsychPlotFrame(wx.Frame):
    def __init__(self, Tmin=263.15, Tmax=333.15, p=101.325, **kwargs):
        wx.Frame.__init__(self, None, title='Psychrometric plot', **kwargs)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.PP = PlotPanel(self)

        self.PP.figure.delaxes(self.PP.ax)
        self.PP.ax = self.PP.figure.add_axes((0.1, 0.1, 0.85, 0.85))

        sizer.Add(self.PP, 1, wx.EXPAND)
        self.SetSizer(sizer)

        PsychChart.p = p
        PsychChart.Tdb = np.linspace(Tmin, Tmax)

        sl = PsychChart.SaturationLine()
        sl.plot(self.PP.ax)

        rhl = PsychChart.HumidityLines([0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
        rhl.plot(self.PP.ax)

        hl = PsychChart.EnthalpyLines(range(-20, 100, 10))
        hl.plot(self.PP.ax)

        pf = PsychChart.PlotFormatting()
        pf.plot(self.PP.ax)

        sizer.Layout()

        self.MenuBar = None
        self.File = None
        self.add_menu()

        self.PP.toolbar = WXToolbar(self.PP.canvas)
        self.PP.toolbar.Realize()
        self.PP.GetSizer().Add(self.PP.toolbar)

        self.PP.Layout()

    def add_menu(self):
        # Menu Bar
        self.MenuBar = wx.MenuBar()
        self.File = wx.Menu()

        mnu_item = wx.MenuItem(self.File, -1, "Edit...", "", wx.ITEM_NORMAL)

        self.File.AppendItem(mnu_item)
        self.MenuBar.Append(self.File, "File")

        self.SetMenuBar(self.MenuBar)


class PHPlotFrame(wx.Frame):
    def __init__(self, Fluid):
        wx.Frame.__init__(self, None, title='p-h plot: ' + Fluid)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.PP = PlotPanel(self, size=(-1, -1))

        sizer.Add(self.PP, 1, wx.EXPAND)
        self.SetSizer(sizer)
        Ph(str(Fluid),
           axis=self.PP.ax,
           Tmin=CP.CoolProp.Props(str(Fluid), 'Ttriple') + 0.01)
        sizer.Layout()

        self.MenuBar = None
        self.File = None
        self.add_menu()

    def add_menu(self):
        # Menu Bar
        self.MenuBar = wx.MenuBar()
        self.File = wx.Menu()

        mnu_item = wx.MenuItem(self.File, -1, "Edit...", "", wx.ITEM_NORMAL)

        self.File.AppendItem(mnu_item)
        self.MenuBar.Append(self.File, "File")

        self.SetMenuBar(self.MenuBar)

    def overlay_points(self):
        pass

    def overlay_cycle(self):
        pass


class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent, ncol=20, nrow=8):
        wx.grid.Grid.__init__(self, parent)

        self.CreateGrid(ncol, nrow)
        [self.SetCellValue(i, j, '0.0') for i in range(20) for j in range(8)]


class SaturationTableDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.FluidLabel = wx.StaticText(self, label="Fluid")
        self.FluidCombo = wx.ComboBox(self)
        self.FluidCombo.AppendItems(sorted(CP.__fluids__))
        self.FluidCombo.SetEditable(False)
        self.TtripleLabel = wx.StaticText(self, label="Critical Temperature [K]")
        self.TtripleValue = wx.TextCtrl(self)
        self.TtripleValue.Enable(False)
        self.TcritLabel = wx.StaticText(self, label="Critical Temperature [K]")
        self.TcritValue = wx.TextCtrl(self)
        self.TcritValue.Enable(False)
        self.NvalsLabel = wx.StaticText(self, label="Number of values")
        self.NvalsValue = wx.TextCtrl(self)
        self.TminLabel = wx.StaticText(self, label="Minimum Temperature [K]")
        self.TminValue = wx.TextCtrl(self)
        self.TmaxLabel = wx.StaticText(self, label="Maximum Temperature [K]")
        self.TmaxValue = wx.TextCtrl(self)

        self.Accept = wx.Button(self, label="Accept")

        sizer = wx.FlexGridSizer(cols=2)
        sizer.AddMany([
            self.FluidLabel, self.FluidCombo,
            self.TtripleLabel, self.TtripleValue,
            self.TcritLabel, self.TcritValue
        ])
        sizer.AddSpacer(10)
        sizer.AddSpacer(10)
        sizer.AddMany([
            self.NvalsLabel, self.NvalsValue,
            self.TminLabel, self.TminValue,
            self.TmaxLabel, self.TmaxValue
        ])
        sizer.Add(self.Accept)

        self.Bind(wx.EVT_COMBOBOX, self.OnSelectFluid)
        self.Bind(wx.EVT_BUTTON, self.OnAccept)

        self.SetSizer(sizer)
        sizer.Layout()
        self.Fit()

        # Bind a key-press event to all objects to get Esc
        children = self.GetChildren()
        for child in children:
            child.Bind(wx.EVT_KEY_UP, self.OnKeyPress)

    def OnKeyPress(self, event=None):
        """ cancel if Escape key is pressed """
        event.Skip()
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.EndModal(wx.ID_CANCEL)

    def get_values(self):
        fluid = str(self.FluidCombo.GetStringSelection())
        if fluid:
            n = float(self.NvalsValue.GetValue())
            tmin = float(self.TminValue.GetValue())
            tmax = float(self.TmaxValue.GetValue())
            tvals = np.linspace(tmin, tmax, n)
            return fluid, tvals
        else:
            return '', []

    def OnCheckTmin(self):
        pass

    def OnCheckTmax(self):
        pass

    def OnAccept(self, event=None):
        self.EndModal(wx.ID_OK)

    def OnSelectFluid(self, event=None):
        fluid = str(self.FluidCombo.GetStringSelection())
        if fluid:
            Tcrit = CP.CoolProp.Props(fluid, 'Tcrit')
            Ttriple = CP.CoolProp.Props(fluid, 'Ttriple')
            self.TcritValue.SetValue(str(Tcrit))
            self.TtripleValue.SetValue(str(Ttriple))
            self.NvalsValue.SetValue('100')
            self.TminValue.SetValue(str(Ttriple + 0.01))
            self.TmaxValue.SetValue(str(Tcrit - 0.01))


class SaturationTable(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.Fluid, self.Tvals = self.OnSelect()
        if self.Fluid:
            self.tbl = SimpleGrid(self, ncol=len(self.Tvals))
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.tbl, 1, wx.EXPAND)
            self.SetSizer(sizer)
            sizer.Layout()
            self.build()

            self.MenuBar = None
            self.File = None
            self.add_menu()
        else:
            self.Destroy()

    @staticmethod
    def OnSelect(event=None):
        fluid = None
        tvals = None
        dlg = SaturationTableDialog(None)
        if dlg.ShowModal() == wx.ID_OK:
            fluid, tvals = dlg.get_values()
        dlg.Destroy()
        return fluid, tvals

    def build(self):
        self.SetTitle('Saturation Table: ' + self.Fluid)
        self.tbl.SetColLabelValue(0, "Temperature\n[K]")
        self.tbl.SetColLabelValue(1, "Liquid Pressure\n[kPa]")
        self.tbl.SetColLabelValue(2, "Vapor Pressure\n[kPa]")
        self.tbl.SetColLabelValue(3, "Liquid Density\n[kg/m3]")
        self.tbl.SetColLabelValue(4, "Vapor Density\n[kg/m3]")

        for i, T in enumerate(self.Tvals):
            fluid = self.Fluid
            p_l = CP.CoolProp.Props('P', 'T', T, 'Q', 0, fluid)
            p_v = CP.CoolProp.Props('P', 'T', T, 'Q', 1, fluid)
            rho_l = CP.CoolProp.Props('D', 'T', T, 'Q', 0, fluid)
            rho_v = CP.CoolProp.Props('D', 'T', T, 'Q', 1, fluid)

            self.tbl.SetCellValue(i, 0, str(T))
            self.tbl.SetCellValue(i, 1, str(p_l))
            self.tbl.SetCellValue(i, 2, str(p_v))
            self.tbl.SetCellValue(i, 3, str(rho_l))
            self.tbl.SetCellValue(i, 4, str(rho_v))

    def add_menu(self):
        # Menu Bar
        self.MenuBar = wx.MenuBar()
        self.File = wx.Menu()

        mnu_item0 = wx.MenuItem(self.File, -1, "Select All \tCtrl+A", "", wx.ITEM_NORMAL)
        mnu_item1 = wx.MenuItem(self.File, -1, "Copy selected data \tCtrl+C", "", wx.ITEM_NORMAL)
        mnu_item2 = wx.MenuItem(self.File, -1, "Copy table w/ headers \tCtrl+H", "", wx.ITEM_NORMAL)

        self.File.AppendItem(mnu_item0)
        self.File.AppendItem(mnu_item1)
        self.File.AppendItem(mnu_item2)
        self.MenuBar.Append(self.File, "Edit")
        self.Bind(wx.EVT_MENU, lambda event: self.tbl.SelectAll(), mnu_item0)
        self.Bind(wx.EVT_MENU, self.OnCopy, mnu_item1)
        self.Bind(wx.EVT_MENU, self.OnCopyHeaders, mnu_item2)

        self.SetMenuBar(self.MenuBar)

    def OnCopy(self, event=None):

        # Number of rows and cols
        rows = self.tbl.GetSelectionBlockBottomRight()[0][0] - self.tbl.GetSelectionBlockTopLeft()[0][0] + 1
        cols = self.tbl.GetSelectionBlockBottomRight()[0][1] - self.tbl.GetSelectionBlockTopLeft()[0][1] + 1

        # data variable contain text that must be set in the clipboard
        data = ''

        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                data += str(self.tbl.GetCellValue(
                    self.tbl.GetSelectionBlockTopLeft()[0][0] + r,
                    self.tbl.GetSelectionBlockTopLeft()[0][1] + c)
                )
                if c < cols - 1:
                    data += '\t'
            data += '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
        event.Skip()

    def OnCopyHeaders(self, event=None):
        self.tbl.SelectAll()
        # Number of rows and cols
        rows = self.tbl.GetSelectionBlockBottomRight()[0][0] - self.tbl.GetSelectionBlockTopLeft()[0][0] + 1
        cols = self.tbl.GetSelectionBlockBottomRight()[0][1] - self.tbl.GetSelectionBlockTopLeft()[0][1] + 1

        # data variable contain text that must be set in the clipboard
        data = ''

        # Add the headers
        for c in range(cols):
            data += str(self.tbl.GetColLabelValue(c).replace('\n', ' '))
            if c < cols - 1:
                data += '\t'
        data += '\n'
        # For each cell in selected range append the cell value in the data variable
        # Tabs '\t' for cols and '\r' for rows
        for r in range(rows):
            for c in range(cols):
                data += str(self.tbl.GetCellValue(
                    self.tbl.GetSelectionBlockTopLeft()[0][0] + r,
                    self.tbl.GetSelectionBlockTopLeft()[0][1] + c)
                )
                if c < cols - 1:
                    data += '\t'
            data += '\n'
        # Create text data object
        clipboard = wx.TextDataObject()
        # Set data object value
        clipboard.SetText(data)
        # Put the data in the clipboard
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(clipboard)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox("Can't open the clipboard", "Error")
        event.Skip()


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None)

        self.MenuBar = None
        self.plots = None
        self.PHPlot = None
        self.TSPlot = None
        self.tables = None
        self.PsychPlot = None
        self.SatTable = None

        self.build()

    def build(self):
        # Menu Bar
        self.MenuBar = wx.MenuBar()

        self.plots = wx.Menu()
        self.PHPlot = wx.Menu()
        self.TSPlot = wx.Menu()
        self.tables = wx.Menu()
        self.PsychPlot = wx.MenuItem(self.plots, -1, 'Psychrometric Plot')
        self.SatTable = wx.MenuItem(self.tables, -1, ' Saturation Table', "", wx.ITEM_NORMAL)

        for Fluid in sorted(CP.__fluids__):
            mnu_item = wx.MenuItem(self.PHPlot, -1, Fluid, "", wx.ITEM_NORMAL)
            self.PHPlot.AppendItem(mnu_item)
            self.Bind(wx.EVT_MENU, lambda event: self.OnPHPlot(event, mnu_item), mnu_item)

            mnu_item = wx.MenuItem(self.TSPlot, -1, Fluid, "", wx.ITEM_NORMAL)
            self.TSPlot.AppendItem(mnu_item)
            self.Bind(wx.EVT_MENU, lambda event: self.OnTSPlot(event, mnu_item), mnu_item)

        self.MenuBar.Append(self.plots, "Plots")
        self.plots.AppendItem(self.PsychPlot)
        self.plots.AppendMenu(-1, 'p-h plot', self.PHPlot)
        self.plots.AppendMenu(-1, 'T-s plot', self.TSPlot)
        self.MenuBar.Append(self.tables, "Tables")
        self.tables.AppendItem(self.SatTable)
        self.Bind(wx.EVT_MENU, self.OnSatTable, self.SatTable)
        self.Bind(wx.EVT_MENU, self.OnPsychPlot, self.PsychPlot)

        self.SetMenuBar(self.MenuBar)

    @staticmethod
    def OnPsychPlot(event=None):

        # Load the options
        dlg = PsychOptions(None)
        if dlg.ShowModal() == wx.ID_OK:
            tmin = float(dlg.Tmin.GetValue()) + 273.15
            tmax = float(dlg.Tmax.GetValue()) + 273.15
            p = float(dlg.p.GetValue())
            ppf = PsychPlotFrame(Tmin=tmin, Tmax=tmax, p=p, size=(1000, 700))
            ppf.Show()
        dlg.Destroy()

    @staticmethod
    def OnSatTable(event):
        tbl = SaturationTable(None)
        tbl.Show()

    def OnPHPlot(self, event, mnuItem):
        # Make a p-h plot instance in a new frame
        # Get the label (Fluid name)
        fluid = self.PHPlot.FindItemById(event.Id).Label
        ph = PHPlotFrame(fluid)
        ph.Show()

    def OnTSPlot(self, event, mnuItem):
        # Make a p-h plot instance in a new frame
        # Get the label (Fluid name)
        fluid = self.TSPlot.FindItemById(event.Id).Label
        ts = TSPlotFrame(fluid)
        ts.Show()


if __name__ == '__main__':
    app = wx.App(False)
    wx.InitAllImageHandlers()

    frame = MainFrame()
    frame.Show(True)
    app.MainLoop()
