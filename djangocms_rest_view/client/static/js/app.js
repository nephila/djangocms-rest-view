var app = angular.module('cmsrest', []);

app.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.filter('safe', function ($sce) {
  return function (val) {
    return $sce.trustAsHtml(val);
  };
});

app.controller('client', function ($scope, $http, $filter) {
  var urlBase = '/api/';

  $scope.renderPage = function (page) {
    if (page != undefined)
      $scope.current_page = page;
    $http.get(urlBase + 'pages/' + $scope.current_page.id)
      .success(function (data) {
        $scope.content_page = data;
      });
  };

  $scope.openPage = function (page_url) {
    $http.get(page_url)
      .success(function (data) {
        $scope.current_page = data;
        $scope.content_page = data;
      });
  };

  $http.get(urlBase + 'pages/')
    .success(function (data) {
      $scope.pages = data;
      if (!$scope.current_page) {
        for (var i = 0; i < data.length; i++) {
          var page = data[i];
          if (page.is_home) {
            $scope.current_page = page;
            break;
          }
        }
      }

      $http.get(urlBase + 'pages/menu/')
        .success(function (data) {
          $scope.menu = data;
          $scope.renderPage()
        });
    });

});

