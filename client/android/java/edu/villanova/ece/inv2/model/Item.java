package edu.villanova.ece.inv2.model;

/**
 * Created by bk on 7/27/15.
 */
public class Item {
    int id;
    String category;
    String manufacturer;
    String model;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public void setManufacturer(String manufacturer) {
        this.manufacturer = manufacturer;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    @Override
    public String toString() {
        return this.manufacturer + " " + this.model + " ("+this.category+")";
    }

    @Override
    public boolean equals( Object obj ) {
        if (obj.getClass() == Item.class) {
            Item i = (Item)obj;
            if (i.getId() == this.getId())
                return true;
            if (i.getCategory().equals(this.getCategory()))
                if (i.getManufacturer().equals(this.getManufacturer()))
                    if (i.getModel().equals(this.getModel()))
                        return true;
        }
        return false;
    }
}
