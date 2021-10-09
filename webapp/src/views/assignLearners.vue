<template>
    
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="viewport" content="width=device-width">

    <title>Assign Learner to Class</title>

    <link rel="stylesheet" href="">
    <!--[if lt IE 9]>
      <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <!-- Bootstrap libraries -->
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
        integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"
        integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut"
        crossorigin="anonymous"></script>

    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"
        integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k"
        crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12/dist/vue.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>

<body>
    <div id="main-container" class="container">
        <h1 class="display-4">Assign a learner to a class</h1>

        <form>
        <h2>Enter Learner Name</h2>

        <div class="form-group">
            <input type="text" class="form-control" id="search-name" v-model="search">
          </div>

          <!-- <div v-for="(value, index) in learners" class="form-check">
            <input class="form-check-input" type="radio" name="learner" v-bind:id="value.id" v-bind:value="value.id" v-model="learner">
            <label class="form-check-label" v-bind:for="value.id">
                <strong>{{ value.title }}</strong> {{ value.name }} – <em>e-wallet balance: ${{ value.ewallet_balance }}</em>
            </label>
          </div> -->

        <h2>Select a class</h2>
        <div v-for="(value, index) in class" class="form-check">
            <input class="form-check-input" type="radio" name="class" v-bind:id="value.id" v-bind:value="value.id" v-model="class_id">
            <!-- <label class="form-check-label" v-bind:for="value.id">
                <strong>{{ value.title }}</strong> {{ value.name }} <em>@ ${{ value.hourly_rate }}/hr</em>
            </label> -->
        </div>

          <!-- <h2>Diagnosis</h2>

          <div class="form-group">
            <input type="text" class="form-control" name="diagnosis" id="diagnosis" v-model="diagnosis">
          </div>

          <h2>Prescription</h2>

          <div class="form-group">
            <input type="text" class="form-control" name="prescription" id="prescription" v-model="prescription">
          </div>

          <h2>Appointment Length</h2>

          <div class="form-group">
            <input type="number" class="form-control" name="length" id="length" v-model="length">
            <small id="length" class="form-text text-muted">Please specify the number of <strong>minutes</strong></small>
          </div>

          <button id="addConsultBtn" class="btn btn-primary" v-on:click="submitForm">Create Consultation</button>
          <p><label id="error" class="text-danger">{{ error }}</label></p>
        </form>

        <p>
            <em><strong>Pages:</strong> <a href="view-consultations.html">View Consultation Records</a></em>
        </p> -->

    </div>
</template>


// <script>
//     Vue.component('person-comp', {
// props: ['id'],
// template: '<span><strong>{{title}}</strong> {{name}}</span>',
// data: function () {
//     return {
//       id: 0,
//       email: '',
//       password: '',
//       first_name:  '',
//       middle_name: '',
//       last_name: '',
//       department_id: '',
//     };
// },
// created: function () {
//     axios.get('http://localhost:5000/api/learners/' + this.id)
//         .then(response => {
//             this.id = response.data.data.id
//             this.password = response.data.data.password
//             this.first_name = response.data.data.first_name
//             this.middle_name = response.data.data.middle_name
//             this.last_name = response.data.data.last_name
//             this.department_id = response.data.data.department_id
//         });
// },
// });

//     const vm = new Vue({
//         el: '#main-container',
//         data: {
//             learners: []
//         },
//         mounted: function() {
//             // axios.get('http://localhost:5000/consultations')
//             //     .then(response => {
//             //         this.consultations = response.data.data;
//             //     })
//             //     .catch(error => alert(error));
//         }
//     });
//
</script>


<script>
import axios from 'axios';
export default {
  name: 'Learner',
  data() {
    return {
    //   email: '',
    //   password: '',
    //   isError: false,
    //   error: '',
      id: 0,
      email: '',
      password: '',
      first_name:  '',
      middle_name: '',
      last_name: '',
      department_id: '',
    };
  },
  methods: {
    async handleLearners(email, password) {
      // Create JSON object to receive the auth
      if (email == '' || password == '') {
        this.isError = true;
        this.error = 'Empty fields';
        return;
      }
      await axios
        .post('/api/auth/learners', {
          email: email,
          password: password,
        })
        .then((response) => {
          this.isError = false;
          const auth = response.data.result.records[0];
          const expiry_seconds = Date.parse(auth.expiry_date);
          // Save to localstorage, so that it can be used to identify users
          window.localStorage.setItem('session_token', auth.token);
          window.localStorage.setItem('token_expiry', expiry_seconds);
          console.log(expiry_seconds);
          // redirect to dashboard
          window.location.replace('/');
        })
        .catch((error) => {
          this.isError = true;
          this.error = error.response.data.result.message;
        });
    },
  },
};
    
    import Login from '@/components/Login.vue';
    export default {
    name: 'Home',
    components: {
        Login,
    },
    created() {
        if (
            window.localStorage.getItem('session_token') &&
            window.localStorage.getItem('token_expiry')
        ) {
            window.location.replace('/');
            }
        },
    };


    const vm = new Vue({
        el: '#main-container',
        data: {
            class: [],
            search: '',
            learners: [],
            class_id: 0,
            learner_id: 0,
            diagnosis: '',
            prescription: '',
            length: '',
            error: ''
        },
        methods: {
            submitForm: function() {
            event.preventDefault();
            axios.post('http://localhost:5000/classes', {
                    doctor_id: this.doctor_id,
                    patient_id: this.patient_id,
                    diagnosis: this.diagnosis,
                    prescription: this.prescription,
                    length: Number(this.length)
                })
            .then(response => {
                    window.location.replace("./view-consultations.html");
                    return false;
                })
            .catch(error => { this.error = error.response.data.message });
            }
        },
        mounted: function() {
            axios.get('http://localhost:5000/api/learners')
                .then(response => {
                    this.learner = response.data.data;
                })
                .catch(error => alert(error));
        }
        watch: {
            search: function() {
                if (this.search === '') {
                    this.patients = []
                } else {
                    axios.get('http://localhost:5000/patients?name=' + this.search)
                    .then(response => {
                        this.patients = response.data.data;
                    })
                    .catch(error => alert(error));
                }
            }
        }
    });
</script>
