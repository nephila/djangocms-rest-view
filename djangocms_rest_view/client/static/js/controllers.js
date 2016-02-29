var restControllers = angular.module('cmsrest.controllers', []);

restControllers.controller('ClientCtrl', ['$scope', '$location', 'restClient', function ($scope, $location, restClient) {

  restClient.boot();

  restClient.getPagesMenu()
    .then(function (res) {
      $scope.menu = res.data;
      if (res.data.length > 0) {
        $location.path('/pages/' + res.data[0].id);
      }
    })

}]);


restControllers.controller('PageDetailCtrl', ['$scope', '$location', '$window', '$routeParams', 'restClient', function ($scope, $location, $window, $routeParams, restClient) {
  $scope.content_page;
  $scope.finishLoading = function() {
    setTimeout(function () {
      $('div[ng-view] a').click(function() {
        event.preventDefault();
        var href = $( this ).attr('href');
        console.log(href);
        restClient.rewriteUrl(href)
          .then(function (newUrl) {
            $location.path(newUrl);
          }, function (newUrl) {
            console.log('Url not found, normal redirect to ' + newUrl);
            $window.location.href = newUrl;
          });

      });
    }, 100);
  };

  restClient.getPage($routeParams.pageId)
    .then(function (res_data) {
      $scope.templateUrl = '/static/partials/' + res_data.data.template;
      $scope.content_page = res_data.data;
    });
}]);