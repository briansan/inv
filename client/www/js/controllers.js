angular.module('inv.controllers', ['ionic', 'inv.services'])

/*
 Root Controller 
*/
.controller('RootCtrl', function($scope, $ionicModal, $timeout, $state, $window, User) {
  //=============
  // login logic
  //=============

  // init login data
  $scope.loginData = {};

  // create login modal view
  $ionicModal.fromTemplateUrl('templates/login.html', {
    scope: $scope,
    // no closing allow :)
    backdropClickToClose: false,
    hardwareBackButtonClose: false
  }).then(function(modal) {
    // set the modal property
    $scope.modal = modal;
  });

  // perform the login action when the user submits the login form
  $scope.doLogin = function(i) {
    // pass the credentials into the user factory
    User.auth(i.username,i.password)
    .then(function(response) { 
      // display the response
      $scope.response = response.data.msg
      $scope.success = response.data.success
      // close the modal dialog if success
      if (response.data.success) {
        $timeout( function() {
          $scope.modal.hide()
        }, 1000);
      }
    }
  )}

  // function to trigger the login view if not logged in
  $scope.$on('$ionicView.enter', function(e) {
    // checking authentication
    User.getSession().success(function(data) {
      // success is false if no session
      if (!data.success) {
        // open a modal controller
        $scope.modal.show()
      }
    })
  });

  $scope.add = function() {
    $state.go('add.inv')
  }
  $scope.logout = function() {
    User.destroySession()
    $window.location.reload(true)
  }
})

/*
Controller for our tab bar
*/
.controller('AddCtrl', function($scope, $ionicModal, $timeout, User, $ionicHistory) {

})

/*
Controller for the Add Inventory page
*/
.controller('AddInvCtrl', function($scope, $state) {
  $scope.cancel = function() {
    $state.go('root');
  }
})

/*
Controller for the Add Asset page
*/
.controller('AddAssetCtrl', function($scope, $state) {
  $scope.cancel = function() {
    $state.go('root');
  }
})

/*
Controller for the Add Item page
*/
.controller('AddItemCtrl', function($scope, $state) {
  $scope.cancel = function() {
    $state.go('root');
  }
})


/*
Controller for the Add Location page
*/
.controller('AddLocationCtrl', function($scope, $state) {
  $scope.cancel = function() {
    $state.go('root');
  }
})
