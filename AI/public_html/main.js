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


        $scope.invert_task = function(task){
            task[2] = !task[2]
        };

        $scope.deliver_taskset = function(name, taskset){

            $http({
                method: 'POST',
                url: "/api/student/deliver_taskset",
                data: {
                    name: name,
                    taskset: taskset
                },
                headers: {'Content-Type': 'application/json'}
            }).success(function(data)
            {

                retrieve_taskset(name)


            });

        };


        var retrieve_taskset = function(key){

            $http.get('/api/student/' + key + '/taskset').success(function(data) {

                $scope.students[key].tags = data.tags;
                $scope.students[key].matrix = data.matrix;
                $scope.students[key].taskset = data.taskset

            });


        };


        $scope.students = function(){
            $http.get('/api/students').success(function(data) {
                $scope.students = data;

                angular.forEach($scope.students, function(value, key){
                    retrieve_taskset(key)
                });


            });
        };
        $scope.students();





    });