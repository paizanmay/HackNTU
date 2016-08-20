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


manageRoom.controller('ManageRoomCtrl', function($scope, RoomResource) {
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

	$scope.detailPage = function(detailUUID) {
		RoomResource.get({'uuid': detailUUID}).$promise.then(function(response){
			$scope.roomDetail = response;
			$scope.changePage(1);
		});
	}

	$scope.handleUpdate = function(roomJson) {
		RoomResource.partial_update({'uuid': roomJson.uuid}, roomJson).$promise.then(function(response){
			$scope.roomDetail = response;
		})
	}

	init();
});
