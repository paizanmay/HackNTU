'use strict';

var manageRoom = angular.module('manageRoom', ['ngResource'])
.config(function($interpolateProvider, $resourceProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
    $resourceProvider.defaults.stripTrailingSlashes = false;
});

manageRoom.factory('$apiResource', ['$resource', function($resource){
    return function(url, paramDefaults, actions){
        var MY_ACTIONS = {
		    'update': {method:'PUT'},
		    'partial_update': {method:'PATCH'}
	    };
	    actions = angular.extend({}, MY_ACTIONS , actions);
	    url = "/landlord/api/"+url;
	    return $resource(url, paramDefaults, actions);
	}
}]);

manageRoom.factory('RoomResource', function($apiResource) {
    return $apiResource('room/:uuid/', null);
});


manageRoom.controller('ManageRoomCtrl', function($scope, $http, RoomResource) {
	function init() {
		$scope.roomList = [];
		$scope.roomDetail = {};
		$scope.currentPage = 0;
		RoomResource.query().$promise.then(function(response){
			$scope.roomList = response;
		});
	}

	$scope.changePage = function(page) {
		$scope.currentPage = page;
	}

	$scope.createRoom = function() {
		var roomData = {
			'name': '房間名稱',
			'rental': 0,
			'landlord_user': $scope.roomList[0].landlord_user
		};
		var room = new RoomResource(roomData)
		room.$save(function(response){
			$scope.roomList.push(response);
		});
	}

	$scope.detailPage = function(detailUUID) {
		RoomResource.get({'uuid': detailUUID}).$promise.then(function(response){
			$scope.roomDetail = response;
			$scope.changePage(1);
			$("#room_qrcode").html("");
			new QRCode(document.getElementById("room_qrcode"), detailUUID);
		});
	}

	$scope.handleUpdate = function(roomJson) {
		RoomResource.partial_update({'uuid': roomJson.uuid}, roomJson).$promise.then(function(response){
			$scope.roomDetail = response;
		})
	}

	$scope.sendPayment = function() {
		var data = {
			'order_detail': {},
			'tenant_allocation': [],
			'user': $scope.roomDetail.landlord_user,
		};

		for(var key in $scope.roomDetail.tenant_user) {
			var tenant_user = $scope.roomDetail.tenant_user[key];
			data['tenant_allocation'].push({
				'amount': tenant_user.live_room_amount,
				'uuid': tenant_user.uuid
			});
		}

		data['order_detail'] = {
			'room': $scope.roomDetail.uuid,
			'order_type': 0,
			'amount': $scope.roomDetail.rental,
		}

		$http.post('/landlord/api/room_order', data).then(function(response){
			console.log('ok')
		});

	}

	init();
});
