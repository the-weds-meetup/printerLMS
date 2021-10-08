<template>

  <div>
    <!-- Start of navbar -->
    <div class="sidebar-container">
      <div class="sidebar-logo">
        LMS - Trainer
      </div>
      <ul class="sidebar-navigation">
        <li class="header">Navigation</li>
        <li>
          <a href="#">Homepage</a>
        </li>
        <li>
          <a href="#">Dashboard</a>
        </li>
        <li class="header">Another Menu</li>
        <li>
          <router-link to="/viewclass">Class list</router-link>
        </li>
        <li>
          <router-link to="/createclass">Create Class</router-link>
        </li>
      </ul>
    </div>

    <!-- End of navbar -->

    <!-- Start of classlist -->
        
     <div class="content-container">
      
        <div class="container-fluid">
      
          <!-- Main component for a primary marketing message or call to action -->
          <h1 class = "center">Class list</h1>
          <div class = "center">
        
        <br>
          
          <h1>Filter Class based on Courseid from DataBase </h1>

        <br>
        
        <form @submit.prevent ="submitform()">
            <input type="text" name="courseid" placeholder="Enter Courseid"/>
            <input type="submit" name=" search" value = "Filter by Courseid"/>
        </form>

        <br><br>
        <table class="table table-dark table-striped">
            <th>Course ID</th>
            <th>ClassID</th>
            <th>Max capacity</th>
            <th>Current capacity</th>
            <th>Start date</th>
            <th>End date</th>
            <th>Enrolment start date</th>
            <th>Enrolment end date</th>
        </table>

        <br><br>
        <h1>All classes listed inside DataBase </h1>
        <br><br>
        <table class="table table-dark table-striped">
            <th>Course ID</th>
            <th>ClassID</th>
            <th>Max capacity</th>
            <th>Current capacity</th>
            <th>Start date</th>
            <th>End date</th>
            <th>Enrolment start date</th>
            <th>Enrolment end date</th>
        </table>
            
          </div>
        </div>
    </div>

    <!-- End of class list -->

  </div>
    
</template>

<script>

export default{
    name: 'viewclass',
    data(){
      return{
        courseid: '',
        classid: '',
        maxcapacity: '',
        currentcapacity: '',
        startdate: '',
        enddate: '',
        enrolstartdate: '',
        enrolenddate: '',
      }
    },
    methods:{
      submitform(){
        console.log("Update!")
      }
    }
    
}

</script>

<style>
@import "../assets/style/style.css";
</style>