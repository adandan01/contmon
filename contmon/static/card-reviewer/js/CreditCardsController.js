(function() {
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
  vm.list = CreditCardsService.get();
}

})();