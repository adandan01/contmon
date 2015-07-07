(function () {
    'use strict';

    /**
     * Users Service
     */
    angular
        .module('myapp')
        .factory('CreditCardsService', Service);

    Service.$inject = [
        '$filter', '$http'
    ];

    function Service($filter, $http) {



        var websites = function () {
            return $http({
                url: '/content/api/websites/',
                method: "GET",
            });
        };

        var list = function () {

            return $http({
                url: '/content/api/creditcards/',
                method: "GET",
                params: {page: 1}
            });
        };
        var list_by_website = function (website) {

            return $http({
                url: '/content/api/creditcards/',
                method: "GET",
                params: {website: website}
            });
        };
        var list_by_page = function (page) {

            return $http({
                url: '/content/api/creditcards/',
                method: "GET",
                params: {page: page}
            });
        };

        var getById = function (id) {
            return $http.get('/content/api/creditcards/' + id + '/');
        };

        var changeReviewState = function (id, review_state) {
            return $http({
                url: '/content/api/creditcards/' + id + '/',
                method: "PATCH",
                data: {review_state: review_state}
            });
        };


        return {
            list: list,
            list_by_page: list_by_page,
            list_by_website: list_by_website,
            changeReviewState: changeReviewState,
            getById: getById,
            websites: websites
        }
    }

})();