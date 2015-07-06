angular
    .module('myapp', [
        'ui.router',
        'ui.layout',
        'infinite-scroll',
        'myapp.home',
        'myapp.creditcards'
    ])

    .config(Config);

Config.$inject = [
    '$urlRouterProvider',
    '$stateProvider',
    '$locationProvider'
];

function Config($urlRouterProvider, $stateProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $urlRouterProvider.otherwise('/home'); // default route

    $stateProvider.state('home', {
        url: '/home',
        templateUrl: 'templates/home.tpl.html',
        controller: 'HomeController',
        controllerAs: 'home'
    })
        .state('creditcards', {
            url: '/creditcards',
            templateUrl: 'templates/creditcards.tpl.html',
            controller: 'CreditCardsController',
            controllerAs: 'creditcards'
        })
        .state('creditcards.details', {
            url: '/:id',
            templateUrl: 'templates/details.tpl.html',
            controller: 'DetailsController',
            controllerAs: 'details'
        });
}