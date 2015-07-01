(function() {
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
  angular.extend(vm, CreditCardsService.getById(parseInt($stateParams.id)));
  console.log(window.location);
}

})();