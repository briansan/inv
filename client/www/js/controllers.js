angular.module('inv.controllers', ['ionic', 'inv.services'])

/*
Controller for our tab bar
*/
.controller('AddCtrl', function($scope, $ionicModal, User) {
  // init login data
  $scope.loginData = {};

  // create login modal used for later
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope
  }).then(function(modal) {
    $scope.modal = modal;
  });

  // triggered in the login modal to close it
  $scope.closeLogin = function() {
    $scope.modal.hide();
  };

  // open the login modal
  $scope.login = function() {
    $scope.modal.show();
  };

  // perform the login action when the user submits the login form
  $scope.doLogin = function() {
    if (User.auth($scope.loginData.username, $scope.loginData.password)) {
      console.log('login success')
    } else {
      console.log('login fail')
    }
  }

  $scope.$on('$ionicView.enter', function(e) {
    // checking authentication
    User.getSession(function(data) {
      // success is false if no session
      if (!data.success) {
        // open a modal controller
        $ionicModal.fromTemplateUrl('templates/login.html', {
          scope: $scope
        }).then(function(modal) {
          modal.show()
        })
      }
    })
  });
})

/*
Controller for the Add Inventory page
*/
.controller('AddInvCtrl', function($scope, User) {
  var logout = function() {
    User.destroySession()
    console.log('logout')
  }
})

/*
Controller for the Add Asset page
*/
.controller('AddAssetCtrl', function($scope) {

})

/*
Controller for the Add Item page
*/
.controller('AddItemCtrl', function($scope) {

})


/*
Controller for the Add Location page
*/
.controller('AddLocationCtrl', function($scope) {

})
