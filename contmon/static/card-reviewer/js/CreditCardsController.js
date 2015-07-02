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

        CreditCardsService.list().success(function (data, status) {

            vm.list = data.results;
        });
        vm.websites = CreditCardsService.websites();
        vm.loadMore = function () {
            console.log('calling load more');
            vm.busy = true;
            console.log('vm.list', vm.list, vm.list.length);
            if (vm.list && vm.list.length > 0) {
                console.log('concating', vm.list.slice(10));
                CreditCardsService.list().success(function (data, status) {
                    vm.list = vm.list.concat(data.results.slice(10));
                    vm.busy = false;
                });
            }

        }

    }

})();