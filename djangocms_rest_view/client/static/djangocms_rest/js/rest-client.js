angular.module('cmsrest.services', [])
  .provider('restClient', function() {

    var urlBase = '/api';
    var urls = {};

    this.setBaseUrl = function (_urlBase) {
      urlBase = _urlBase;
    }

    function RestClientService($q, $http, $filter) {

      var pathFilter = $filter('nphPath');

      this.boot = function () {
        var deferred = $q.defer();
        urls = {};
        return $http.get(
          urlBase + '/pages/urls'
        ).then(function(res) {
          var data = res.data;
          for (var i = 0 ; i < data.length ; i++) {
            urls[pathFilter('/', data[i].absolute_url)] = data[i].pk;
          }
          console.log(urls);
          deferred.resolve();
        }, function(res) {
          deferred.reject();
        });
        return deferred.promise;
      };

      this.rewriteUrl = function (url) {
        var deferred = $q.defer();
        var id = urls[pathFilter('/', url)];
        console.log(id);

        if (id) {
          deferred.resolve('/pages/' + id);
        } else {
          deferred.reject(url);
        }
        return deferred.promise;
      };

      this.getPage = function (pageId) {
        return $http.get(
          urlBase + '/pages/' + pageId
        )
      };

      this.getPages = function () {
        return $http.get(
          urlBase + '/pages/'
        )
      };

      this.getPagesMenu = function () {
        return $http.get(
          urlBase + '/pages/menu/'
        )
      };

      this.getPageContent = function (pageUrl) {
        return $http.get(
          pageUrl
        )
      };

      this.loadTemplate = function (templateName) {
        return $http.get(
          '/static/partials/' + templateName
        )
      };

    }

    this.$get = ['$q', '$http', '$filter', function monetasServiceFactory($q, $http, $filter) {
      return new RestClientService($q, $http, $filter);
    }];

  });
