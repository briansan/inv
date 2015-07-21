var json2form = function(json) {
  var y = [];
  for (var x in json) {
    y.push(encodeURIComponent(x) + '=' + encodeURIComponent(json[x]));
  }
  return y.join('&');
}

angular.module('inv.services', ['ngResource'])

.factory('User', function($http, SERVER) {
  // api method url constants
  var login = SERVER.url + '/login';
  var logout = SERVER.url + '/logout';
  var get = SERVER.url + '/view/user';
  var set = SERVER.url + '/edit/user';

  // user group enumeration
  var Groups = {
    0: 'No Group',
    1: 'Student',
    2: 'Faculty',
    3: 'Operator',
    4: 'Admin'
  }
  // user object definition
  var o = {
    id: 0,
    uname: 'Anonymous',
    fname: 'Anony',
    lname: 'mous',
    grp: 0,
    perm: 0,
    start: null
  }


  // authentication method
  o.auth = function(uname,passwd) {
    // try to login through server
    return $http.post(login, json2form({uname:uname, passwd:passwd})).success(function(data) {
      // if successful, set the user data
      if (data.success) { 
        y = o.storeSession(); 
      }
    });
  }

  // stores user data into session obj
  o.storeSession = function() {
    // get the user data
    o.getSession().success(function(data){
      var x = data.msg;
      o.id = x.id;
      o.fname = x.fname;
      o.lname = x.lname;
      o.grp = x.grp;
      o.perm = x.perm;
      o.start = x.start;
    });
  }

  // get session
  o.getSession = function() {
    // make the request
    return $http.get(SERVER.url).success(function(){});
  }

  // logging out
  o.destroySession = function() {
    var y = false;
    $http.post(logout).success(function(data) {
      y = data.success;
    });
    return y;
  }

  return o;
});
