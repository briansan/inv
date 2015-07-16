//
// @file   inv/js/api.js
// @author Brian Kim
// @brief  a script that defines an api handler using jquery
//

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
  this.add_location = function(building, room, callback) {
    data = {building:building,room:room};
    this.inv_ajax('/add/location','POST',data,callback);
  }

  this.get_location = function(id,callback) {
    this.inv_ajax('/view/location/'+id,'GET',null,callback);
  }

  this.get_location_all = function(callback) {
    this.inv_ajax('/view/location','GET',null,callback);
  }

  this.set_location = function(id,building,room,callback) {
    data = {building:building,room:room};
    this.inv_ajax('/edit/location/'+id,'POST',data,callback);
  }

  this.delete_location = function(id,callback) {
    this.inv_ajax('/delete/location/'+id,'GET',null,callback);
  }
};
