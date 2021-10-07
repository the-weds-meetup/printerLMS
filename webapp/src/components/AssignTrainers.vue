<template>
  <div class="container" id="main-container">
    <form v-bind:style="{paddingTop: '20px'}">
        <!-- Select trainer name -->
        <div class="form-group mb-3">
            <div v-bind:style="{textAlign: 'left'}">
                <label for="selectTrainer" class="form-label" v-bind:style="{display: 'block'}">Select Trainer</label>
            </div>
            <select class="form-select" id="selectTrainer" v-model="user_id">
                <option v-for="trainer in trainers" v-bind:key="trainer.id" v-bind:value="trainer.id">{{trainer.first_name}}</option>
            </select>
        </div>

        <!-- select course name -->
        <div class="form-group mb-3">
            <div v-bind:style="{textAlign: 'left'}">
                <label for="selectCourse" class="form-label" v-bind:style="{display: 'block'}">Select Course</label>
            </div>
            <select class="form-select" id="selectCourse" v-model="course_id">
                <option v-for="course in courses" v-bind:key="course.id" v-bind:value="course.id">{{course.name}}</option>
            </select>
        </div>

        <!-- select class -->
        <div class="form-group mb-3">
            <div v-bind:style="{textAlign: 'left'}">
                <label for="selectClass" class="form-label" v-bind:style="{display: 'block'}">Select Class</label>
            </div>
            <select class="form-select" id="selectClass" v-model="class_id">
                <option v-for="each_class in classes" v-bind:key="each_class.class_id" v-bind:value="each_class.class_id">Class {{each_class.class_id}}: starting date {{each_class.class_start_date.substring(0, 10)}}</option>
                <option v-if="classes.length == 0" disabled>No classes currently available for this course</option>
            </select>
        </div>

        <button type="button" class="btn btn-primary" v-on:click="assignTrainer" v-bind:disabled="user_id == 0 || course_id == 0 || class_id == 0 || classes.length == 0">Assign Trainer</button>
    </form>
       
</div>
</template>


<script>
    import axios from 'axios';
    
    export default {
        name: "AssignTrainers",
        data() {
            return {
                trainers: [],
                courses: [],
                classes: [],
                user_id: 0,
                course_id: 0,
                class_id: 0,
                trainer_name: "",
                selected_trainer: [],
                department_id: 2,
                error: "",
                isDisable: ""
            }
        },
        methods:{
            assignTrainer: function(){
                axios.post('http://localhost:5000/api/trainer/assign_trainer', {
                    user_id: this.user_id,
                    course_id: this.course_id,
                    class_id: this.class_id,
                    //trainer_name: this.trainer_name
                })
                .then(response => {
                    console.log(response);
                })
                .catch(error => { this.error = error.response.data.message });
            }
        },
        mounted: function(){
            //for now, we assume all learners in the engineer department can be trainers
            axios.get('http://localhost:5000/api/learners/get_trainers/' + this.department_id)
                .then(response => {
                    this.trainers = response.data.data;
                })
                .catch(error => alert(error));
            
            axios.get('http://localhost:5000/api/course/get_courses')
                .then(response => {
                    this.courses = response.data.data;
                })
                .catch(error => alert(error));
        
        },
        //get classes according to course selected
        watch: {
            course_id: function(){
                axios.get('http://localhost:5000/api/classes/get_classes_by_course/' + parseInt(this.course_id))
                .then(response => {
                    this.classes = response.data.data;
                    //reset class_id whenever a new course is selected
                    this.class_id = 0
                })
                .catch(error => alert(error));
            },
        }
    }
</script>