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

createOrder.factory('RoomResource', function($apiResource) {
    return $apiResource('/landlord/api/room/:uuid/', null);
});


function allocateMoney(amount, userList, amountKey) {
    if(!amountKey) {
        amountKey = 'amount';
    }
    var allocation = parseInt(amount / userList.length);
    var lastAllocation = amount - (userList.length * allocation);
    angular.forEach(userList, function(user){
        user[amountKey] = allocation;
    });
    userList[0][amountKey] += lastAllocation;

    return userList;
}

createOrder.controller('createOrderCtrl', function($scope, $http, TenantUserResource) {
    function init() {
        $scope.userList = user_list;
        $scope.orderDetail = {
            'room': roomUuid,
        };
        $scope.isSuccess = false;
        $scope.isPopover = false;
        TenantUserResource.get({'uuid': userUuid}).$promise.then(function(response){
            $scope.user = response
        });
    }

    $scope.allocate = function() {
        if($scope.orderDetail.amount) {
            $scope.userList = allocateMoney($scope.orderDetail.amount, $scope.userList)
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
            'user': $scope.user,
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

});


createOrder.controller('changeRoomFeeCtrl', function($scope, $http, TenantUserResource, RoomResource) {
    $scope.room = null;
    RoomResource.get({'uuid': roomUuid}).$promise.then(function(response){
        $scope.room = response;
    });

    $scope.isSuccess = false;
    $scope.isPopover = false;

    $scope.closePopup = function() {
        $scope.isPopover = false;
        window.close();
    }

    $scope.allocate = function() {
        $scope.room.tenant_user = allocateMoney($scope.room.rental, $scope.room.tenant_user, 'live_room_amount');
    }

    $scope.submit = function() {
        $scope.isPopover = true;
        $http.post('/tenant/api/change_room_fee', {'room': $scope.room, 'user_uuid': userUuid}).then(function(response){
            $scope.room = response;
            $scope.isSuccess = true;
        });
    }


});
