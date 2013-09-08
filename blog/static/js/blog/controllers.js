var appController = Blog.controller('AppController', function ($scope, $rootScope, $location, GlobalService) {
    var failureCb = function (status) {
        console.log(status);
    };
    $scope.globals = GlobalService;
 
    $scope.initialize = function (is_authenticated) {
        $scope.globals.is_authenticated = is_authenticated;
    };
})

// Manages a list of posts and create new ones
Blog.controller('FeedController', function ($scope, GlobalService, PostService, posts) {
    $scope.posts = posts;
    $scope.globals = GlobalService;
    //options for modals
    $scope.opts = {
        backdropFade: true,
        dialogFade: true
    };
    //open modals
    $scope.open = function (action) {
        if (action === 'create'){
            $scope.postModalCreate = true;
            $scope.post = new Object();
        };
    };
    //close modals
    $scope.close = function (action) {
        if (action === 'create'){
            $scope.postModalCreate = false;
        };
    };
    //calling board service
    $scope.create = function () {
        PostService.save($scope.post).then(function (data) {
            $scope.post = data;
            $scope.posts.push(data);
            $scope.postModalCreate = false;
        }, function(status){
            console.log(status);
        });
    };
});

// Read and Edit a single post
Blog.controller('PostController', function ($scope, $routeParams, $location, PostService, GlobalService, post) {
    $scope.post = post;
    $scope.globals = GlobalService;
    var failureCb = function (status) {
        console.log(status);
    }
    //options for modals
    $scope.opts = {
        backdropFade: true,
        dialogFade: true
    };
    //open modals
    $scope.open = function (action) {
        $scope.postName = $scope.post.name;
        $scope.postDescription = $scope.post.description;
        if (action === 'edit'){
            $scope.postModalEdit = true;
        };
    };
    //close modals
    $scope.close = function (action) {
        $scope.postName = "";
        $scope.postDescription = "";
        if (action === 'edit'){
            $scope.postModalEdit = false;
        };
    };
    //calling board service
    $scope.update = function () {
        PostService.update($scope.post).then(function (data) {
            $scope.post = data;
            $scope.postModalEdit = false;
        }, failureCb);
    };
});