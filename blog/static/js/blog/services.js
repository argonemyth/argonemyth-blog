Blog.factory('GlobalService', function () {
    var vars = {
        is_authenticated: false
    }
    return vars;
});


Blog.factory('PostService', function ($http, $q) {
    var api_url = "/blog/api/posts/";
    return {
        get: function (post_slug) {
            var url = api_url + post_slug + "/";
            var defer = $q.defer();
            $http({method: 'GET', url: url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                })
                .error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        list: function () {
            var defer = $q.defer();
            $http({method: 'GET', url: api_url}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        update: function (post) {
            var url = api_url + post.slug + "/";
            var defer = $q.defer();
            $http({method: 'PUT',
                url: url,
                data: post}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
        save: function (post) {
            var url = api_url;
            var defer = $q.defer();
            $http({method: 'POST',
                url: url,
                data: post}).
                success(function (data, status, headers, config) {
                    defer.resolve(data);
                }).error(function (data, status, headers, config) {
                    defer.reject(status);
                });
            return defer.promise;
        },
    }
});
