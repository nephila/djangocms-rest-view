angular.module('cmsrest.filters', [])
  .filter('safe', ['$sce', function ($sce) {
    return function (val) {
      return $sce.trustAsHtml(val);
    };
  }]);
