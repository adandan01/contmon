(function () {
    'use strict';

    /**
     * Users Service
     */
    angular
        .module('myapp')
        .factory('CreditCardsService', Service);

    Service.$inject = [
        '$filter'
    ];

    function Service($filter) {
        var creditcards = [{
            id: 1,
            name: 'Chase Freedom',
            categories: ['0-apr', 'miles', 'student'],
            website: 'bankrate.com',
            urls: ['bestcredit.html', 'free-miles-credit.html'],

        }, {
            id: 2,
            name: 'Chase Freedom',
            categories: ['reward', 'miles'],
            website: 'bankrate.com',
            urls: ['bestcredit.html', 'reward-miles-credit.html'],
        }, {
            id: 3,
            name: 'Citi Diamon',
            categories: ['0-apr', 'miles', 'student'],
            website: 'cardhub.com',
            urls: ['bestcredit.html', 'free-miles-credit.html'],

        }, {
            id: 4,
            name: 'Discover it',
            categories: ['reward', 'miles'],
            website: 'creditkarma.com',
            urls: ['bestcredit.html', 'reward-miles-credit.html'],
        }];

        var list = function () {
            return creditcards;
        };

        var getById = function (id) {
            if (!id) return {};
            return $filter('filter')(creditcards, {id: id}, true)[0] || {};
        };
        var websites = function () {
            var websites = {};
            for (var i=0;i< creditcards.length;i++) {
                websites[creditcards[i].website] = true;
            }
            console.log('websites', Object.keys(websites));
            return Object.keys(websites)
        };

        return {
            list: list,
            getById: getById,
            websites: websites
        }
    }

})();