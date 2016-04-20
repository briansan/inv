


package edu.villanova.ece.inv.manager;

import android.os.AsyncTask;
import android.util.Log;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;

import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.model.Inventory;
import edu.villanova.ece.inv.model.Item;
import edu.villanova.ece.inv.model.Label;
import edu.villanova.ece.inv.model.Location;
import edu.villanova.ece.inv.model.User;

/**
 * Created by bk on 8/3/15.
 */
public class DataManager implements ApiManager.AddMethodDelegate, ApiManager.GetMethodDelegate,
        ApiManager.GetAllMethodDelegate, ApiManager.SetMethodDelegate, ApiManager.RemoveMethodDelegate
{
    // constants
    public static final String TAG = "DataManager";

    //
    // public methods
    //

    //
    // accessor methods

    public void setToken( String t ) { this.token = t; }
    public void setDelegate( DataDelegate delegate ) {
        this.delegate = delegate;
    }

    // get one
    public User getUser(String id) {return this.userMap.get(id);}
    public Item getItem(int id) {return this.itemMap.get(id);}
    public Location getLocation(int id) {return this.locationMap.get(id);}
    public Asset getAsset(String tag) {return this.assetMap.get(tag);}
    public Inventory getInv(int id) {return this.invMap.get(id);}
    public Label.ItemCategory getCategory(String name) {return this.getCategoryMap().get(name);}
    public Label.ItemManufacturer getManufacturer(String name) {return this.getManufacturerMap().get(name);}
    public Label.LocationBuilding getBuilding(String name) {return this.getBuildingMap().get(name);}

    // get all
    public ArrayList<User> getUsers() {return this.users;}
    public ArrayList<Label.ItemCategory> getCategories() {return categories;}
    public ArrayList<Label.ItemManufacturer> getManufacturers() {return manufacturers;}
    public ArrayList<Label.LocationBuilding> getBuildings() {return buildings;}
    public ArrayList<Item> getItems() {return items;}
    public ArrayList<Location> getLocations() {return locations;}
    public ArrayList<Asset> getAssets() {return assets;}
    public ArrayList<Inventory> getInvs() {return invs;}

    public HashMap<String, User> getUserMap() {return userMap;}
    public HashMap<Integer, Item> getItemMap() {return itemMap;}
    public HashMap<Integer, Location> getLocationMap() {return locationMap;}
    public HashMap<String, Asset> getAssetMap() {return assetMap;}
    public HashMap<String, Label.ItemCategory> getCategoryMap() {return categoryMap;}
    public HashMap<String, Label.ItemManufacturer> getManufacturerMap() {return manufacturerMap;}
    public HashMap<String, Label.LocationBuilding> getBuildingMap() {return buildingMap;}

    public HashMap<String, ArrayList<Item>> getCategoryItemMap() {return categoryItemMap;}
    public HashMap<String, ArrayList<Item>> getManufacturerItemMap() {return manufacturerItemMap;}
    public HashMap<String, ArrayList<Location>> getBuildingLocationMap() {return buildingLocationMap;}
    public HashMap<Item, ArrayList<Asset>> getItemAssetMap() {return itemAssetMap;}
    public HashMap<Location, ArrayList<Asset>> getLocationAssetMap() {return locationAssetMap;}
    public HashMap<User, ArrayList<Asset>> getUserAssetMap() {return userAssetMap;}
    public HashMap<Integer, Inventory> getInvMap() {return invMap;}
    public HashMap<Asset, ArrayList<Inventory>> getAssetInvMap() {return assetInvMap;}
    public HashMap<User, ArrayList<Inventory>> getUserInvMap() {return userInvMap;}

    public ArrayList <Asset> getAssetsForItem( Item i) {
        ArrayList<Asset> y = new ArrayList<>();
        for (Asset a : this.assets) {
            if (a.getCurrent().equals(i)){
                y.add(a);
            }
        }
        return y;
    }

    public ArrayList<Asset> getAssetsForLocation( Location loc ) {
        ArrayList<Asset> y = new ArrayList<>();
        for (Asset a : this.assets) {
            if (a.getCurrent().equals(loc)){
                y.add(a);
            }
        }
        return y;
    }
    public ArrayList<Inventory> getInvsForAsset( Asset a ) {
        ArrayList<Inventory> y = new ArrayList<>();
        for (Inventory inv : this.invs) {
            if (inv.getWhat().equals(a)) {
                y.add(inv);
            }
        }

        return y;
    }

    public ArrayList<String> getCategoryStrings() {
        ArrayList<Label.ItemCategory> x = getCategories();
        ArrayList<String> y = new ArrayList<>(x.size());
        for (Label.ItemCategory l : x) {
            y.add(l.getName());
        }
        return y;
    }
    public ArrayList<String> getManufacturerStrings() {
        ArrayList<Label.ItemManufacturer> x = getManufacturers();
        ArrayList<String> y = new ArrayList<>(x.size());
        for (Label.ItemManufacturer l : x) {
            y.add(l.getName());
        }
        return y;
    }
    public ArrayList<String> getBuildingStrings() {
        ArrayList<Label.LocationBuilding> x = getBuildings();
        ArrayList<String> y = new ArrayList<>(x.size());
        for (Label.LocationBuilding l : x) {
            y.add(l.getName());
        }
        return y;
    }
    public ArrayList<String> getItemStrings() {
        ArrayList<Item> x = getItems();
        ArrayList<String> y = new ArrayList<>(x.size());
        for (Item i : x) {
            y.add(i.toString() + "("+i.getCategory()+")");
        }
        return y;
    }

    //
    // utility methods

    public int init()
    {
        this.token = AuthManager.getToken();

        manufacturers = null;
        categories = null;
        items = null;
        buildings = null;
        locations = null;
        users = null;
        assets = null;
        invs = null;

        ApiManager.getEntityAll(User.class, token, this);
        ApiManager.getEntityAll(Item.class, token, this);
        ApiManager.getEntityAll(Location.class, token, this);
        ApiManager.getEntityAll(Asset.class, token, this);
        ApiManager.getEntityAll(Inventory.class, token, this);
        ApiManager.getEntityAll(Label.ItemManufacturer.class, token, this);
        ApiManager.getEntityAll(Label.ItemCategory.class, token, this);
        ApiManager.getEntityAll(Label.LocationBuilding.class, token, this);
        return 8;
    }

    public void sortItemsByManufacturer() {
        Collections.sort(items, new Comparator<Item>() {
            @Override
            public int compare(Item i1, Item i2) {
                return i1.getManufacturer().compareTo(i2.getManufacturer());
            }
        });
    }

    public interface DataDelegate {
        public void downloadingDidProgress(String msg);
        public void downloadingDidComplete();
        public void processingDidProgress(String msg);
        public void processingDidComplete();
        public void failure(int code, String reason);
    }

    //
    // instance variables
    private DataDelegate delegate;
    private String token;
    private User user;

    private ArrayList<Label.ItemManufacturer> manufacturers;
    private ArrayList<Label.ItemCategory> categories;
    private ArrayList<Item> items;
    private ArrayList<Label.LocationBuilding> buildings;
    private ArrayList<Location> locations;
    private ArrayList<User> users;
    private ArrayList<Asset> assets;
    private ArrayList<Inventory> invs;

    private HashMap<Integer, Item> itemMap;
    private HashMap<Integer, Location> locationMap;
    private HashMap<String, User> userMap;
    private HashMap<String, Asset> assetMap;
    private HashMap<Integer,Inventory> invMap;
    private HashMap<String, Label.ItemCategory> categoryMap;
    private HashMap<String, Label.ItemManufacturer> manufacturerMap;
    private HashMap<String, Label.LocationBuilding> buildingMap;

    private HashMap<String,ArrayList<Item>> categoryItemMap;
    private HashMap<String,ArrayList<Item>> manufacturerItemMap;
    private HashMap<String,ArrayList<Location>> buildingLocationMap;
    private HashMap<Item,ArrayList<Asset>> itemAssetMap;
    private HashMap<Location,ArrayList<Asset>> locationAssetMap;
    private HashMap<User,ArrayList<Asset>> userAssetMap;
    private HashMap<Asset,ArrayList<Inventory>> assetInvMap;
    private HashMap<User,ArrayList<Inventory>> userInvMap;

    //
    // private api
    //

    public int processData() {

        final ArrayList<Item> allItems = this.items;
        final ArrayList<Label.ItemCategory> allCategories = this.categories;
        final ArrayList<Label.ItemManufacturer> allManufacturers = this.manufacturers;
        final ArrayList<Label.LocationBuilding> allBuildings = this.buildings;
        final ArrayList<Asset> allAssets = this.assets;
        final ArrayList<Location> allLocations = this.locations;
        final ArrayList<User> allUsers = this.users;
        final ArrayList<Inventory> allInvs = this.invs;

        buildingLocationMap = new HashMap<String,ArrayList<Location>>(allBuildings.size());
        categoryItemMap = new HashMap<String,ArrayList<Item>>(allCategories.size());
        manufacturerItemMap = new HashMap<String,ArrayList<Item>>(allManufacturers.size());
        itemAssetMap = new HashMap<Item,ArrayList<Asset>>(allItems.size());
        locationAssetMap = new HashMap<Location,ArrayList<Asset>>(allLocations.size());
        assetInvMap = new HashMap<Asset,ArrayList<Inventory>>(allAssets.size());
        userAssetMap = new HashMap<User,ArrayList<Asset>>(allUsers.size());
        userInvMap = new HashMap<User,ArrayList<Inventory>>(allUsers.size());

        categoryMap = new HashMap<String, Label.ItemCategory>(allAssets.size());
        manufacturerMap = new HashMap<String, Label.ItemManufacturer>(allAssets.size());
        buildingMap = new HashMap<String, Label.LocationBuilding>(allAssets.size());
        itemMap = new HashMap<Integer, Item>(allItems.size());
        locationMap = new HashMap<Integer, Location>(allLocations.size());
        assetMap = new HashMap<String, Asset>(allAssets.size());
        userMap = new HashMap<String, User>(allUsers.size());
        invMap = new HashMap<Integer, Inventory>(allInvs.size());

        (new AsyncTask() {
            @Override
            protected Object doInBackground(Object[] params) {

                // map out the categories
                for (Label.ItemCategory i: allCategories) {
                    categoryMap.put(i.getName(),i);
                }
                if (delegate != null) delegate.processingDidProgress("Categories Mapped");

                // map out the manufacturesr
                for (Label.ItemManufacturer i: allManufacturers) {
                    manufacturerMap.put(i.getName(), i);
                }
                if (delegate != null) delegate.processingDidProgress("Manufacturers Mapped");

                // map out the buildings
                for (Label.LocationBuilding i: allBuildings) {
                    buildingMap.put(i.getName(), i);
                }
                if (delegate != null) delegate.processingDidProgress("Buildings Mapped");

                // map out the items
                for (Item i: allItems) {
                    itemMap.put(i.getId(),i);
                }
                if (delegate != null) delegate.processingDidProgress("Items Mapped");

                // map out the locations
                for (Location i: allLocations) {
                    locationMap.put(i.getId(), i);
                }
                if (delegate != null) delegate.processingDidProgress("Locations Mapped");

                // map out the locations
                for (User i: allUsers) {
                    userMap.put(i.getUid(), i);
                }
                if (delegate != null) delegate.processingDidProgress("Users Mapped");

                // map out the assets
                for (Asset i: allAssets) {
                    assetMap.put(i.tag_ece, i);
                }
                if (delegate != null) delegate.processingDidProgress("Assets Mapped");

                // map out the invs
                for (Inventory i: allInvs) {
                    invMap.put(i.getId(), i);
                }
                if (delegate != null) delegate.processingDidProgress("Inventories Mapped");

                // map out the categories to the items
                for (Label.ItemCategory category : categories) {
                    ArrayList<Item> items = new ArrayList<Item>();
                    categoryItemMap.put(category.getName(), items);
                }

                for (Item i : allItems) {
                    String cat = i.getCategory();
                    categoryItemMap.get(cat).add(i);
                }
                if (delegate != null) delegate.processingDidProgress("Categories Mapped to Items");

                // map out the manufacturers to the items
                for (Label.ItemManufacturer man : manufacturers) {
                    ArrayList<Item> items = new ArrayList<Item>();
                    manufacturerItemMap.put(man.getName(), items);
                }

                for (Item i : allItems) {
                    String man = i.getManufacturer();
                    manufacturerItemMap.get(man).add(i);
                }
                if (delegate != null) delegate.processingDidProgress("Manufacturers Mapped to Items");

                // map out the buildings to the locations
                for (Label.LocationBuilding building : buildings) {
                    ArrayList<Location> locations = new ArrayList<Location>();
                    buildingLocationMap.put(building.getName(), locations);
                }

                for (Location i : allLocations) {
                    String b = i.getBuilding();
                    buildingLocationMap.get(b).add(i);
                }
                if (delegate != null) delegate.processingDidProgress("Buildings Mapped to Locations");

                // map out the items to the assets
                for (Item i: items) {
                    // set empty lists as the value for each item
                    ArrayList<Asset> assets = new ArrayList<Asset>();
                    itemAssetMap.put(i, assets);
                }

                for (Asset a : allAssets) {
                    // add the asset to the list corresponding to the item
                    Item i = a.getItem();
                    itemAssetMap.get(i).add(a);
                }
                if (delegate != null) delegate.processingDidProgress("Items Mapped to Assets");

                // map out the locations to the assets
                for (Location l: locations) {
                    // set empty lists as the value for each location
                    ArrayList<Asset> assets = new ArrayList<Asset>();
                    locationAssetMap.put(l, assets);
                }

                for (Asset a : allAssets) {
                    // add the asset to the list corresponding to the location
                    Location l = locationMap.get(a.home);
                    locationAssetMap.get(l).add(a);
                }
                if (delegate != null) delegate.processingDidProgress("Locations Mapped to Assets");

                // map out the assets to the inventories
                for (Asset asset : assets) {
                    // set empty lists as the value for each asset
                    ArrayList<Inventory> invs = new ArrayList<Inventory>();
                    assetInvMap.put(asset, invs);
                }

                for (Inventory inv: allInvs) {
                    // add the inv to the list corresponding to the asset
                    Asset a = inv.getWhat();
                    assetInvMap.get(a).add(inv);
                }
                if (delegate != null) delegate.processingDidProgress("Assets Mapped to Inventories");

                // map out the users to the assets
                for (User u : allUsers) {
                    // set empty lists as the value for each asset
                    ArrayList<Asset> assets = new ArrayList<Asset>();
                    userAssetMap.put(u, assets);
                }

                for (Asset asset: allAssets) {
                    // add the inv to the list corresponding to the asset
                    User a = userMap.get(asset.owner);
                    userAssetMap.get(a).add(asset);
                }
                if (delegate != null) delegate.processingDidProgress("Users Mapped to Assets");

                // map out the users to the inventories
                for (User u : allUsers) {
                    // set empty lists as the value for each asset
                    ArrayList<Inventory> invs = new ArrayList<Inventory>();
                    userInvMap.put(u, invs);
                }

                for (Inventory inv: allInvs) {
                    // add the inv to the list corresponding to the asset
                    User a = inv.getWho();
                    userInvMap.get(a).add(inv);
                }
                if (delegate != null) delegate.processingDidProgress("Users Mapped to Inventories");

                if (delegate != null) delegate.processingDidComplete();

                return null;
            }
        }).execute();

        return 16;
    }

    public boolean downloadComplete() {
        return (users!=null&&items!=null&&invs!=null&&locations!=null&&assets!=null&&categories!=null&&manufacturers!=null&&buildings!=null);
    }

    //
    // delegate methods

    @Override
    public void gotEntity(Object obj) {

    }

    @Override
    public void gotEntityAll(Class type, ArrayList obj) {

        String msg = "";
        if (type == Item.class) {this.items = obj; msg = "Items loaded";}
        else if (type == Location.class) {this.locations = obj; msg = "Locations loaded";}
        else if (type == User.class) {this.users = obj; msg = "Users loaded";}
        else if (type == Asset.class) {this.assets = obj; msg = "Assets loaded";}
        else if (type == Inventory.class) {this.invs= obj; msg = "Invs loaded"; }
        else if (type == Label.ItemCategory.class) {this.categories = obj; msg = "Categories loaded"; }
        else if (type == Label.ItemManufacturer.class) {this.manufacturers = obj; msg = "Manufacturers loaded"; }
        else if (type == Label.LocationBuilding.class) {
            this.buildings = obj; this.buildings.add(new Label.LocationBuilding());
            msg = "Buildings loaded";
        }
        else {
            msg = "empty list";
        }

        Log.d(TAG,msg);
        //
        // report to the delegate of the data loading
        if (this.delegate != null) this.delegate.downloadingDidProgress(msg);

        if (downloadComplete() && delegate!=null) this.delegate.downloadingDidComplete();
    }

    @Override
    public void getEntityFailed(int code, String info) {
        if (this.delegate != null) this.delegate.failure(code, info);
    }

    @Override
    public void setEntityFailure(int code, String reason) {
        if (this.delegate != null) this.delegate.failure(code, reason);
        if (this.modDelegate != null) modDelegate.saveFailure(code, reason);
    }

    @Override
    public void addEntityFailure(int code, String reason) {
        if (this.delegate != null) this.delegate.failure(code, reason);
        if (this.modDelegate != null) modDelegate.saveFailure(code, reason);
    }

    @Override
    public void removeEntitySuccess(String msg) {
        if (this.modDelegate != null) modDelegate.deleteSuccess(msg);
    }

    @Override
    public void removeEntityFailure(int code, String reason) {

        if (this.delegate != null) this.delegate.failure(code,reason);
        if (this.modDelegate != null) modDelegate.saveFailure(code, reason);
    }

    //
    // modification methods

    public void rmItem(Item i) {
        ApiManager.deleteEntity(Item.class,i.getId(),this.token,this);
    }

    public void rmLocation(Location i) {
        ApiManager.deleteEntity(Location.class,i.getId(),this.token,this);
    }

    public void rmAsset(Asset i) {
        ApiManager.deleteEntity(Asset.class,i.getTag_ece(),this.token,this);
    }

    public void rmUser(User i) {
        ApiManager.deleteEntity(User.class,i.getUid(),this.token,this);
    }

    public void rmInv(Inventory i) {
        ApiManager.deleteEntity(Inventory.class,i.getId(),this.token,this);
    }

    public void saveItem(Item i) {
        if (i.getId() != 0) {
            ApiManager.setEntity(Item.class,i.getId(),i,this.token,this);
        } else {
            ApiManager.addEntity(Item.class,i,this.token,this);
        }
    }

    public void saveLocation(Location i) {
        if (i.getId() != 0) {
            ApiManager.setEntity(Location.class, i.getId(), i, this.token, this);
        } else {
            ApiManager.addEntity(Location.class,i,this.token,this);
        }
    }

    public void saveAsset(Asset i) {
        if (getAsset(i.getTag_ece()) != null) {
            ApiManager.setEntity(Asset.class, i.getTag_ece(), i, this.token, this);
        } else {
            ApiManager.addEntity(Asset.class,i,this.token,this);
        }
    }

    public void saveUser(User i) {
        if (getUser(i.getUid()) != null) {
            ApiManager.setEntity(User.class, i.getUid(), i, this.token, this);
        } else {
            ApiManager.addEntity(User.class,i,this.token,this);
        }
    }

    public void saveInv(Inventory i) {
        if (i.getId() != 0) {
            ApiManager.setEntity(Inventory.class, i.getId(), i, this.token, this);
        } else {
            ApiManager.addEntity(Inventory.class,i,this.token,this);
        }
    }

    public void addLabel(Label i, Class type) {
        ApiManager.addEntity(type, i, this.token, this);
    }

    @Override
    public void setEntitySuccess(Object obj) {
        if (obj.getClass() == Item.class) {
            // set the new item values within the data structures
            Item newItem = (Item)obj;
            Item myItem = this.getItem(newItem.getId());
            myItem.setModel(newItem.getModel());
            myItem.setManufacturer(newItem.getManufacturer());
            myItem.setCategory(newItem.getCategory());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == Location.class) {
            // set the new item values within the data structures
            Location newItem = (Location)obj;
            Location myItem = this.getLocation(newItem.getId());
            myItem.setBuilding(newItem.getBuilding());
            myItem.setRoom(newItem.getRoom());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == Asset.class) {
            // set the new item values within the data structures
            Asset newItem = (Asset)obj;
            Asset myItem = this.getAsset(newItem.getTag_ece());
            myItem.setItem(newItem.getItem().getId());
            myItem.setStatus(newItem.getStatus());
            myItem.setTag_vu(newItem.getTag_vu());
            myItem.setTag_svc(newItem.getTag_svc());
            myItem.setTag_unit(newItem.getTag_unit());
            myItem.setSerial(newItem.getSerial());
            myItem.setPurchased(newItem.getPurchased());
            myItem.setOwner(newItem.getOwner().getUid());
            myItem.setHome(newItem.getHome().getId());
            myItem.setPrice(newItem.getPrice());
            myItem.setIp(newItem.getIp());
            myItem.setComments(newItem.getComments());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == User.class) {
            // set the new user values within the data structures
            User newUser = (User)obj;
            User myUser = this.getUser(newUser.getUid());
            myUser.setFname(newUser.getFname());
            myUser.setLname(newUser.getLname());
            myUser.setEmail(newUser.getEmail());
            myUser.setPhone(newUser.getPhone());
            myUser.setPerm(newUser.getPerm());
            myUser.setGrp(newUser.getGrp());
            if (this.modDelegate != null) modDelegate.saveSuccess(newUser);
        }
        else if (obj.getClass() == Inventory.class) {
            // set the new user values within the data structures
            Inventory newInv= (Inventory)obj;
            Inventory myInv = this.getInv(newInv.getId());
            myInv.setWho(newInv.getWho().getUid());
            myInv.setWhat(newInv.getWhat().getTag_ece());
            myInv.setWhen(newInv.getWhen().getTime());
            myInv.setWhere(newInv.getWhere().getId());
            myInv.setHow(newInv.getHow());
            if (this.modDelegate != null) modDelegate.saveSuccess(newInv);
        }
    }

    @Override
    public void addEntitySuccess(Object obj) {
        if (obj.getClass() == Item.class) {
            // add the new item values into the data structures
            Item newItem = (Item) obj;
            this.items.add(newItem);
            this.itemMap.put(newItem.getId(), newItem);
            this.categoryItemMap.get(newItem.getCategory()).add(newItem);
            this.manufacturerItemMap.get(newItem.getManufacturer()).add(newItem);
            this.itemAssetMap.put(newItem, new ArrayList<Asset>());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == Location.class) {
            // add the new item values into the data structures
            Location newItem = (Location) obj;
            this.locations.add(newItem);
            this.locationMap.put(newItem.getId(), newItem);
            this.buildingLocationMap.get(newItem.getBuilding()).add(newItem);
            this.locationAssetMap.put(newItem, new ArrayList<Asset>());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == Asset.class) {
            // add the new item values into the data structures
            Asset newItem = (Asset) obj;
            this.assets.add(newItem);
            this.assetMap.put(newItem.getTag_ece(), newItem);
            this.locationAssetMap.get(newItem.getHome()).add(newItem);
            this.itemAssetMap.get(newItem.getItem()).add(newItem);
            this.userAssetMap.get(newItem.getOwner()).add(newItem);
            this.assetInvMap.put(newItem, new ArrayList<Inventory>());
            if (this.modDelegate != null) modDelegate.saveSuccess(newItem);
        }
        else if (obj.getClass() == User.class) {
            // set the new user values within the data structures
            User newUser = (User)obj;
            this.users.add(newUser);
            this.userMap.put(newUser.getUid(), newUser);
            this.userAssetMap.put(newUser, new ArrayList<Asset>());
            this.userInvMap.put(newUser, new ArrayList<Inventory>());
            if (this.modDelegate != null) modDelegate.saveSuccess(newUser);
        }
        else if (obj.getClass() == Inventory.class) {
            // set the new user values within the data structures
            Inventory newInv = (Inventory)obj;
            this.invs.add(newInv);
            this.invMap.put(newInv.getId(), newInv);
            this.assetInvMap.get(newInv.getWhat()).add(newInv);
            this.userInvMap.get(newInv.getWho()).add(newInv);
            if (this.modDelegate != null) modDelegate.saveSuccess(newInv);
        }
        else if (obj.getClass() == Label.ItemCategory.class) {
            Label.ItemCategory newCat = (Label.ItemCategory)obj;
            this.categories.add(newCat);
            this.categoryMap.put(newCat.getName(), newCat);
            this.categoryItemMap.put(newCat.getName(), new ArrayList<Item>());
        }
        else if (obj.getClass() == Label.ItemManufacturer.class) {
            Label.ItemManufacturer newCat = (Label.ItemManufacturer)obj;
            this.manufacturers.add(newCat);
            this.manufacturerMap.put(newCat.getName(), newCat);
            this.manufacturerItemMap.put(newCat.getName(), new ArrayList<Item>());
        }
        else if (obj.getClass() == Label.LocationBuilding.class) {
            Label.LocationBuilding newCat = (Label.LocationBuilding)obj;
            this.buildings.add(newCat);
            this.buildingMap.put(newCat.getName(), newCat);
            this.buildingLocationMap.put(newCat.getName(), new ArrayList<Location>());
        }
    }

    private ModificationDelegate modDelegate;
    public void setModDelegate(ModificationDelegate del) {this.modDelegate = del;}

    public interface ModificationDelegate {
        void saveSuccess(Object obj);
        void deleteSuccess(String msg);
        void saveFailure(int code, String reason);
    }

    //
    // singleton stuff
    //
    private static DataManager obj;
    private DataManager() {}
    public static DataManager sharedManager() {
        if (obj == null) {
            obj = new DataManager();
        }
        return obj;
    }

}
