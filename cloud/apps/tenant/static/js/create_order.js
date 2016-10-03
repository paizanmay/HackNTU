'use strict';

var createOrder = angular.module('createOrder', ['ngResource'])
.config(function($interpolateProvider, $resourceProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    $resourceProvider.defaults.stripTrailingSlashes = false;
});

createOrder.factory('$apiResource', ['$resource', function($resource){
    return function(url, paramDefaults, actions){
        var MY_ACTIONS = {
            'update': {method:'PUT'},
            'partial_update': {method:'PATCH'}
        };
        actions = angular.extend({}, MY_ACTIONS , actions);
        // url = "/landlord/api/"+url;
        return $resource(url, paramDefaults, actions);
    }
}]);

createOrder.factory('TenantUserResource', function($apiResource) {
    return $apiResource('/tenant/api/tenant_user/:uuid/', null);
});


createOrder.controller('createOrderCtrl', function($scope, $http) {
    function init() {
        $scope.userList = user_list;
        $scope.orderDetail = {
            'room': roomUuid,
        };
        $scope.isSuccess = false;
        $scope.isPopover = false;
    }

    $scope.allocate = function() {
        if($scope.orderDetail.amount) {
            var allocation = $scope.orderDetail.amount / $scope.userList.length;
            angular.forEach($scope.userList, function(user){
                user.amount = allocation;
            });
        }
    }

    $scope.closePopup = function() {
        $scope.isPopover = false;
        window.close();
    }

    $scope.create = function() {
        $scope.isPopover = true;
        var data = {
            'order_detail': $scope.orderDetail,
            'tenant_allocation': $scope.userList,
            'user_uuid': userUuid,
        }
        $http.post('/landlord/api/room_order', data)
        .then(function(response){
            $scope.isSuccess = true;
        });
    }

    init();
});

createOrder.controller('accountSettingCtrl', function($scope, $http, TenantUserResource) {
    $scope.user = user;
    $scope.isSuccess = false;
    $scope.isPopover = false;

    $scope.closePopup = function() {
        $scope.isPopover = false;
        window.close();
    }

    $scope.submit = function() {
        $scope.isPopover = true;
        var data = {
            'bank_code': $scope.user.bankCode,
            'bank_account': $scope.user.bankAccount
        };
        
        TenantUserResource.partial_update({'uuid': $scope.user.uuid}, data).$promise
        .then(function(response){
            $scope.isSuccess = true;
        })
    }


})