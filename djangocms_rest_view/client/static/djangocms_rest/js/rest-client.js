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

      this.loadSekizaiResources = function (sekizais, sekizaiConfig) {
        var rawScripts = [];
        var scriptsLoaded = 0;
        var scriptsToLoad = 0;
        for (var sekizai of sekizais) {
          for (var key in sekizai) {
            for (var element of sekizai[key]) {

              if (sekizaiConfig[key].action == LOAD_JS_SCRIPT) {
                rawScripts.push(element);
              }

              if (sekizaiConfig[key].action == LOAD_JS_FILE) {
                $('head').append('<script src="' + '/' + sekizaiConfig[key].source + '/' + element + '"></script>');
              }

              if (sekizaiConfig[key].action == LOAD_CSS_FILE) {
                $('<link>',{rel:'stylesheet',type:'text/css','href':'/' + sekizaiConfig[key].source + '/' + element}).appendTo('head');
              }

            }

          }
        }

        for (var rawScript of rawScripts) {
          if (!(rawScript.indexOf('<script>') != -1)) {
            $('head').append('<script>' + rawScript + '</script>');
          }
        }

      };

    }

    this.$get = ['$q', '$http', '$filter', function monetasServiceFactory($q, $http, $filter) {
      return new RestClientService($q, $http, $filter);
    }];

  });
