(function() {
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

function Service($filter){
  var creditcards = [{
      id: 34,
      name: 'batman',
      categories: ['admin', 'user']
    }, {
      id: 67,
      name: 'spiderman',
      categories: ['user']
    }];
  
  var get = function() {
    return creditcards;
  }
  
  var getById = function(id) {
    if(!id) return {};
    return $filter('filter')(creditcards, {id:id}, true)[0] || {};
  }

  return {
    get: get,
    getById: getById
  }
}

})();