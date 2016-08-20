'use strict';
$( document ).ready(function(){

var mainView = new Vue({
    el: '#main-view',

    data: function() {
        return {
            isLiveIn: false,
        }
    },

    methods: {
        handleRegister: function() {
            var self = this;
            var post_data = {
                'tenant_id': tenant_id,
                'room_id': room_id
            };

            Vue.http.post('/tenant/api/register_room/', post_data).then(function(response){
                self.isLiveIn = true;
            });
        }
    }
});

});