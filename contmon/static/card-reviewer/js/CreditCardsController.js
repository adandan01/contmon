(function () {
    'use strict';

    /**
     * Users Controller
     */
    angular
        .module('myapp.creditcards')
        .controller('CreditCardsController', Controller);

    Controller.$inject = [
        'CreditCardsService'
    ];

    function Controller(CreditCardsService) {
        console.log("CreditCard controller instantiated");
        var vm = this;
        vm.busy = true;
        vm.list = [];
        vm.page = 1;

        CreditCardsService.list().success(function (data, status) {

            vm.list = data.results;
            vm.busy = false;
        });
        CreditCardsService.websites().success(function (data, status) {
            vm.websites = data;
        });
        vm.filterByWebsite = function (website) {
            console.log('filtering by webiste', website);
            vm.busy = true;
            vm.list = [];
            CreditCardsService.list_by_website(website).success(function (data, status) {

                vm.list = data.results;
                vm.busy = false;
            });
        }
        ;
        vm.loadMore = function () {
            console.log('calling load more');
            vm.busy = true;
            console.log('vm.list', vm.list, vm.list.length);
            if (vm.list && vm.list.length > 0) {

                console.log('loading more');
                CreditCardsService.list_by_page(vm.page).success(function (data, status) {
                    vm.list = vm.list.concat(data.results);
                    vm.busy = false;
                    vm.page = vm.page + 1;
                });
            }

        }

    }

})();