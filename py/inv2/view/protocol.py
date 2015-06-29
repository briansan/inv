"""
  @file   protocols.py
  @author Brian Kim
  @brief  a script that defines all the delegates and datasources
          for the inv interface
"""

class AuthenticationInterface():
    class Delegate():
        def Login(self):
            pass
        def Register(self):
            pass
        def Quit(self):
            pass

class AuthorizationInterface():
    class Delegate():
        def CheckPermission(self):
            pass

class MainInterface():
    class Delegate():
        def ViewItems(self):
            pass
        def AddAssets(self):
            pass
        def Loans(self):
            pass
        def Locations(self):
            pass
        def GenerateReport(self):
            pass
        def Settings(self):
            pass
        def Logout(self):
            pass

class ListInterface():
    class DataSource():
        def NumberOfSections(self):
            pass
        def ElementAtIndexPath(self,i):
            pass
    class Delegate():
        def Back(self):
            pass
        def DidSelectElementAtIndexPath(self,i):
            pass

class InvInterface():
    class Delegate():
        def Back(self):
            pass
        def ViewAll(self):
            pass
        def GenerateReport(self):
            pass

class LoanInterface():
    class Delegate(InvInterface.Delegate):
        def CreateRequest(self):
            pass
        def ProcessLoan(self):
            pass

class LocationInterface():
    class Delegate(InvInterface.Delegate):
        def AddLocation(self):
            pass

class InfoInterface():
    class Delegate():
        def Back(self):
            pass
        def Edit(self):
            pass
        def GenerateReport(self):
            pass

class AssetInfoInterface():
    class DataSource():
        def

    class Delegate(InfoInterface.Delegate):
        def RequestLoan(self):
            pass

class LoanInfoInterface():
    class Delegate(InfoInterface.Delegate):
        def WhichProcess(self):
            pass
        def Process(self):
            pass
