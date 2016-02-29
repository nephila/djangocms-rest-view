var app = angular.module('cmsrest', ['ngNephila', 'ngRoute', 'cmsrest.services', 'cmsrest.filters', 'cmsrest.controllers']);

app.config(['$httpProvider', '$routeProvider', function ($httpProvider, $routeProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $routeProvider.
    when('/', {
      templateUrl: '/static/partials/main.html',
    }).
    when('/pages/:pageId', {
      template: '<article ng-include="templateUrl" onload="finishLoading()"></article>',
      controller: 'PageDetailCtrl'
    }).
    otherwise({
      redirectTo: '/'
    });
}]);