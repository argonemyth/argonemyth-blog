'use strict';

// Since both Angular and Django use double braces, we need to set a new rule for
// Angular to separate between them.
var Blog = angular.module("Blog", ["ngCookies", "ngSanitize", "truncate"], function ($interpolateProvider) {
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");
    }
);

// Sets the CSRF token, this needs angular-cookies.js
Blog.run(function ($http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
})

// Routing for our app
Blog.config(function ($routeProvider) {
    $routeProvider
        .when("/", {
            templateUrl: "partials/posts.html",
            controller: "PostsController",
            resolve: {
                posts: function (PostService) {
                    return PostService.list();
                }
            }
        })
        .when("/post/:slug", {
            templateUrl: "partials/post.html",
            controller: "PostController",
            resolve: {
                post: function ($route, PostService) {
                    var postSlug = $route.current.params.slug
                    return PostService.get(postSlug);
                }
            }
        })
        .when("/post/:slug/edit/", {
            templateUrl: "partials/post_form.html",
            controller: "EditController",
            resolve: {
                post: function ($route, PostService) {
                    var postSlug = $route.current.params.slug
                    return PostService.get(postSlug);
                }
            }
        })
        .otherwise({
            redirectTo: '/blog/'
        })
})
