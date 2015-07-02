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
        vm.images = [1, 2, 3, 4, 5, 6, 7, 8];
        vm.list = CreditCardsService.list();
        vm.websites = CreditCardsService.websites();

    }

})();