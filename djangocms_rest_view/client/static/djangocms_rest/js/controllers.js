var restControllers = angular.module('cmsrest.controllers', []);

restControllers.controller('ClientCtrl', ['$scope', '$location', '$routeParams', 'restClient', function ($scope, $location, $routeParams, restClient) {

  restClient.boot();

  restClient.getPagesMenu()
    .then(function (res) {
      $scope.menu = res.data;
      if (res.data.length > 0) {
        $location.path('/pages/' + ($routeParams.pageId || res.data[0].id));
      }
    })

}]);


restControllers.controller('PageDetailCtrl', ['$scope', '$location', '$window', '$routeParams', 'restClient', function ($scope, $location, $window, $routeParams, restClient) {
  $scope.content_page;
  $scope.sekizais;

  LOAD_JS_FILE = 0;
  LOAD_JS_SCRIPT = 1;
  LOAD_CSS_FILE = 2;

  var sekizaiConfig = {
    'js-media': {
      'action': LOAD_JS_FILE,
      'source': 'media'
    },
    'css-media': {
      'action': LOAD_CSS_FILE,
      'source': 'media'
    },
    'css-screen': {
      'action': LOAD_CSS_FILE,
      'source': 'static'
    },
    'script_ready': {
      'action': LOAD_JS_SCRIPT
    },
    'js': {
      'action': LOAD_JS_SCRIPT
    },
    'js-script': {
      'action': LOAD_JS_FILE,
      'source': 'static'
    },
  }

  $scope.finishLoading = function() {
    setTimeout(function () {
        $(document).ready(function() {
          restClient.loadSekizaiResources(
            $scope.sekizais, sekizaiConfig
          );
      });

      $('div[ng-view] a').click(function() {
        var myEvent = event;
        myEvent.preventDefault();
        var href = $( this ).attr('href');
        console.log(href);
        var that = this;
        restClient.rewriteUrl(href)
          .then(function (newUrl) {
            $location.path(newUrl);
          }, function (newUrl) {
            console.log('Url not found, normal redirect to ' + newUrl);
            this.dispatchEvent(myEvent);
          });

      });
    }, 100);
  };

  restClient.getPage($routeParams.pageId)
    .then(function (res_data) {
      $scope.templateUrl = '/static/partials/' + res_data.data.template;
      $scope.sekizais = res_data.data.placeholders.sekizai;
      $scope.content_page = res_data.data;
    }, function() {console.log("bog")});
}]);