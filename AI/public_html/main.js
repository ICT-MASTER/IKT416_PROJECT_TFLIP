/**
 * Created by perar on 11.11.2015.
 */



var app = angular
    .module('tflip.adaptivlearn', [])
    //.config(config)
    //.run(run);

    /**
     * The main controller for the app. The controller:
     * - retrieves and persists the model via the todoStorage service
     * - exposes the model to the template and provides event handlers
     */
    .controller('appController', function AppController($scope, $http)
    {

        $scope.studentClean = function(){
            $http.get('/api/clean_students').success(function(data) {
                $.notify(data.message);

                $scope.students = {}

            });
        };

        $scope.studentCreate = function(){
            $http.get('/api/create_students').success(function(data) {
                $.notify(data.message);

                $scope.students = data.students
            });
        };

        $scope.students = function(){
            $http.get('/api/students').success(function(data) {
                $scope.students = data;
            });
        };
        $scope.students();





    });