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
        def Add(self):
            pass
        def Locations(self):
            pass
        def Users(self):
            pass
        def Settings(self):
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

class LocationInterface():
    class Delegate(InvInterface.Delegate):
        def AddLocation(self):
            pass

class AssetInterface():
    class Delegate(InvInterface.Delegate):
        def AddAsset(self):
            pass

class InfoInterface():
    class Delegate():
        def Back(self):
            pass
        def Edit(self):
            pass
        def GenerateReport(self):
            pass
        def Save(self,info): # info is a dict
            pass

class LocationInfoInterface(InfoInterface):
    class DataSource():
        def Building(self):
            pass
        def Room(self):
            pass
        def Station(self):
            pass

class ItemInfoInterface(InfoInterface):
    class DataSource():
        def Category(self):
            pass
        def Manufacturer(self):
            pass
        def Model(self):
            pass

class UserInfoInterface(InfoInterface):
    class DataSource():
        def Username(self):
            pass
        def Password(self):
            pass
        def FirstName(self):
            pass
        def LastName(self):
            pass
        def PhoneNumber(self):
            pass
        def Group(self):
            pass
    class Delegate(InfoInterface.Delegate):
        def ViewInventory(self):
            pass

class AssetInfoInterface(InfoInterface):
    class DataSource():
        def Tag(self):
            pass
        def Status(self):
            pass
        def Item(self):
            pass
        def PurchaseDate(self):
            pass
        def ImagePath(self):
            pass
        def Price(self):
            pass
        def ReceiptPath(self):
            pass
        def IPAddress(self):
            pass
        def Comments(self):
            pass
        def Location(self):
            pass

    class Delegate(InfoInterface.Delegate):
        def DoInventory(self):
            pass
        def ViewInventory(self):
            pass

class AssetTagInfoInterface(InfoInterface):
    class DataSource():
        def ECE(self):
            pass
        def VU(self):
            pass
        def UNIT(self):
            pass
        def Service(self):
            pass
        def Serial(self):
            pass
