# Basic website example using Bootstrap 3
Demonstrates a simple website with a top navigation using `ui-router`.

##AngularJS Features
- Modules:
  - ui-router
- Directives:  
  - ng-controller (using controller as notation)
  - ui-sref-active
  - ui-view
  - ui-sref

##Structure
- There are two sections:
  - Homepage, 'Home' section with route: `/` or `/home`. 
  - Users list, 'Users' seciton with route `/users`. Displays a User list.

#Versions
- 3.0 
  - ui-router version
- 2.0 
  - Added child route `users/:id` to users
- 1.0
  - Added Bootstrap 3 responsive navigation bar
  - Added `isActive(route)` to highlight active section
  - Applied [John Papas Guidelines](https://github.com/johnpapa/angular-styleguide) to code

#More Information
You can read a post explaining more details [here](http://bit.ly/ngNewRouter)