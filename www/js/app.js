(function() {
  var app = angular.module('inv',[])

  var server = 'http://vecr.ece.villanova.edu:8000';

  app.controller('APIController', function($scope,$http,$sce) {
    this.data = null; 
    this.login = null;
    self=this;

    $http.get(server).
    success(function(data,status,headers,config) {
      self.data = data.msg;
    }).     
    error(function(data,status,headers,config) {
    });     

    $http.get(server+'/login').
    success(function(data,status,headers,config) {
      self.login = $sce.trustAsHtml(data)
    }).
    error(function(data,status,headers,config) {
    });
  });     
})(); 
