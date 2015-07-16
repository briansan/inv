//
// @file   inv/js/api.js
// @author Brian Kim
// @brief  a script that defines an api handler using jquery
//

//
// convenience methods for making the model objects
// (probably should be placed elsewhere...)
//
var build_location = function(building,room) {
  return {building:building,room:room};
}

var build_item = function(category,manufacturer,model) {
  return {category:category,manufacturer:manufacturer,model:model};
}

var build_asset = function(ece,vu,unit,svc,serial,
                           status,item,purchased,img,
                           owner,holder,price,receipt,
                           ip,comments,home,current) {
  return {
    tag_ece:ece, tag_vu:vu, tag_unit:unit, tag_svc:svc, tag_serial:serial,
    status:status, item:item, purchased:purchased, img:img, owner:owner,
    holder: holder, price:price, receipt:receipt, ip:ip, comments:comments,
    home: home, current:current
  }
}

var build_inv = function(who,what,when,where) {
  return {who:who,what:what,when:when,where:where}
}

var APIController = function(server) {
  // initialization
  if (server == null) server = 'http://vecr.ece.villanova.edu:8000';
  this.server = server;

  // setup the http calls so that the session is maintained
  $.ajaxSetup({xhrFields:{withCredentials:true}});

  // a convenience method to make ajax calls to inv
  this.inv_ajax = function(route,type,data,callback) {
    $.ajax({
      type:type,
      url:this.server+route,
      data:data,
      success:callback
    });
  }

  // login
  this.login = function(uname,passwd,callback) {
    data = { uname:uname, passwd:passwd };
    this.inv_ajax('/login','POST',data,callback);
  }

  // logout
  this.logout = function(callback) {
    this.inv_ajax('/logout','GET',null,callback);
  }

  // methods
  this.methods = function(callback) {
    this.inv_ajax('/','GET',null,callback);
  }

  // user groups
  this.get_user_groups = function(callback) {
    this.inv_ajax('/view/user/group','GET',null,callback);
  }

  // asset statuses
  this.get_asset_statuses = function(callback) {
    this.inv_ajax('/view/asset/status','GET',null,callback);
  }

  // buildings
  this.add_building = function(name, callback) {
    data = {name:name}
    this.inv_ajax('/add/building','POST',data,callback);
  }

  this.get_building_all = function(callback) {
    this.inv_ajax('/view/building','GET',null,callback);
  }

  this.set_building = function(id,name,callback) {
    data = {name:name};
    this.inv_ajax('/edit/building/'+id,'POST',data,callback);
  }

  this.delete_building = function(id,callback) {
    this.inv_ajax('/rm/building/'+id,'GET',null,callback);
  }

  // categories
  this.add_category = function(name, callback) {
    data = {name:name};
    this.inv_ajax('/add/category','POST',data,callback);
  }

  this.get_category_all = function(callback) {
    this.inv_ajax('/view/category','GET',null,callback);
  }

  this.set_category = function(id,name,callback) {
    data = {name:name};
    this.inv_ajax('/edit/category/'+id,'POST',data,callback);
  }

  this.delete_category = function(id,callback) {
    this.inv_ajax('/rm/category/'+id,'GET',null,callback);
  }

  // manufacturers
  this.add_manufacturer = function(name, callback) {
    data = {name:name};
    this.inv_ajax('/add/manufacturer','POST',data,callback);
  }

  this.get_manufacturer_all = function(callback) {
    this.inv_ajax('/view/manufacturer','GET',null,callback);
  }

  this.set_manufacturer = function(id,name,callback) {
    data = {name:name};
    this.inv_ajax('/edit/manufacturer','POST',data,callback);
  }

  this.delete_manufacturer = function(id,callback) {
    this.inv_ajax('/rm/manufacturer','GET',null,callback);
  }

  // location
  this.add_location = function(location, callback) {
    this.inv_ajax('/add/location','POST',location,callback);
  }

  this.get_location = function(id,callback) {
    this.inv_ajax('/view/location/'+id,'GET',null,callback);
  }

  this.get_location_all = function(callback) {
    this.inv_ajax('/view/location','GET',null,callback);
  }

  this.set_location = function(id,location,callback) {
    data = {building:building,room:room};
    this.inv_ajax('/edit/location/'+id,'POST',location,callback);
  }

  this.delete_location = function(id,callback) {
    this.inv_ajax('/delete/location/'+id,'GET',null,callback);
  }

  // item
  this.add_item = function(item,callback) {
    this.inv_ajax('/add/item','POST',item,callback);
  };

  this.get_item = function(id,callback) {
    this.inv_ajax('/view/item/'+id,'GET',null,callback);
  };

  this.get_item_all = function(callback) {
    this.inv_ajax('/view/item','GET',null,callback);
  };

  this.set_item = function(id,item,callback) {
    this.inv_ajax('/edit/item/'+id,'POST',item,callback);
  };

  this.delete_item = function(id,callback) {
    this.inv_ajax('/rm/item/'+id,'GET',null,callback);
  };

  // asset
  this.add_asset = function(asset,callback) {
    this.inv_ajax('/add/asset','POST',asset,callback);
  };

  this.get_asset = function(id,callback) {
    this.inv_ajax('/view/asset/'+id,'GET',null,callback);
  };

  this.get_asset_all = function(callback) {
    this.inv_ajax('/view/asset','GET',null,callback);
  };

  this.set_asset = function(id,asset,callback) {
    this.inv_ajax('/edit/asset','POST',asset,callback);
  };

  this.delete_asset = function(id,callback) {
    this.inv_ajax('/rm/asset','GET',null,callback);
  };

  // inv
  this.add_inv = function(inv,callback) {
    this.inv_ajax('/add/inv','POST',inv,callback);
  };

  this.get_inv = function(id,callback) {
    this.inv_ajax('/view/inv/'+id,'GET',inv,callback);
  };

  this.get_inv_all = function(callback) {
    this.inv_ajax('/view/inv','GET',null,callback);
  };

  this.set_inv = function(id,inv,callback) {
    this.inv_ajax('/edit/inv/'+id,'POST',inv,callback);
  };

  this.delete_inv = function(id,callback) {
    this.inv_ajax('/rm/inv/'+id,'GET',callback);
  };

};
