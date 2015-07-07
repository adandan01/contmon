(function () {
    'use strict';

    /**
     * Details Controller
     */
    angular
        .module('myapp.details')
        .controller('DetailsController', Controller);

    Controller.$inject = [
        'CreditCardsService',
        '$stateParams'
    ];

    function Controller(CreditCardsService, $stateParams) {
        console.log("Details controller");
        var vm = this;
        CreditCardsService.getById(parseInt($stateParams.id)).success(function(data, status) {
            angular.extend(vm, data);
        });

        console.log(window.location);
        vm.markCompliant = function() {

        };
        vm.markNotCompliant = function() {

        };
        vm.markIgnore = function() {

        };
        vm.markReviewState = function(review_state) {

        };
    }

})();