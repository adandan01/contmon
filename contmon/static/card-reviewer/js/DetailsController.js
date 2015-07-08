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
        vm.id = parseInt($stateParams.id);
        function getDetails() {
            CreditCardsService.getById(vm.id).success(function (data, status) {
                angular.extend(vm, data);
            });
        }
        getDetails();


        console.log(window.location);
        vm.markCompliant = function () {
            CreditCardsService.changeReviewState(vm.id, 1).success(function (data, status) {
                console.log('review state change successfully');
                angular.extend(vm, data);
                getDetails();
            });
        };
        vm.markNotCompliant = function () {
            CreditCardsService.changeReviewState(vm.id, 2).success(function (data, status) {
                console.log('review state change successfully');
                angular.extend(vm, data);
                getDetails();
            });
        };
        vm.markIgnore = function () {
            CreditCardsService.changeReviewState(vm.id, 3).success(function (data, status) {
                console.log('review state change successfully');
                angular.extend(vm, data);
                getDetails();
            });

        };
        vm.markReviewState = function (review_state) {

        };
    }

})();