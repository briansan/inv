// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('inv', ['ionic', 'inv.controllers'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if(window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
    

  });
})


.config(function($stateProvider, $urlRouterProvider, $httpProvider) {

  $httpProvider.defaults.withCredentials = true;
  $httpProvider.defaults.headers.post = {'Content-Type': 'application/x-www-form-urlencoded'}

  // Ionic uses AngularUI Router, which uses the concept of states.
  // Learn more here: https://github.com/angular-ui/ui-router.
  // Set up the various states in which the app can be.
  // Each state's controller can be found in controllers.js.
  $stateProvider

  // root controller
  .state('root', {
    url: '/',
    templateUrl: 'templates/root.html',
    controller: 'RootCtrl'
  })

  // Set up an abstract state for the tabs directive:
  .state('add', {
    url: '/add',
    abstract: true,
    templateUrl: 'templates/add.html',
    controller: 'AddCtrl',
    
  })

  // Each tab has its own nav history stack:

  .state('add.item', {
    url: '/item',
    views: {
      'add-item': {
        templateUrl: 'templates/item-form.html',
        controller: 'AddItemCtrl'
      }
    }
  })

  .state('add.location', {
      url: '/location',
      views: {
        'add-location': {
          templateUrl: 'templates/location-form.html',
          controller: 'AddLocationCtrl'
        }
      }
    })

  .state('add.asset', {
      url: '/asset',
      views: {
        'add-asset': {
          templateUrl: 'templates/asset-form.html',
          controller: 'AddAssetCtrl'
        }
      }
    })

  .state('add.inv', {
      url: '/inv',
      views: {
        'add-inv': {
          templateUrl: 'templates/inv-form.html',
          controller: 'AddInvCtrl'
        }
      }
    })
  // If none of the above states are matched, use this as the fallback:
  $urlRouterProvider.otherwise('/');

})


.constant('SERVER', {
  // inv API server
  url: 'http://vecr.ece.villanova.edu:8000'
})
.constant('AUTH_EVENTS', {
  loginSuccess: 'auth-login-success',
  loginFailed: 'auth-login-failed',
  logoutSuccess: 'auth-logout-success',
  sessionTimeout: 'auth-session-timeout',
  notAuthenticated: 'auth-not-authenticated',
  notAuthorized: 'auth-not-authorized'
})
;
