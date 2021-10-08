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
        
    <div class="content-container">
      <div class="container-fluid">
        <h1 class ="center">Create Class</h1>
        <div>
          <!-- Start of form -->
          <form class ="center" @submit.prevent ="submitform()"><br><br>
              Course ID: <input type = "text" v-model ="courseid" placeholder ="Course ID" required> <br><br>
              Class ID: <input type = "text" v-model ="classid" placeholder ="Class ID" required> <br><br>
              Max Capacity: <input type = "number" v-model ="maxcapacity" placeholder = "Max Capacity"> <br><br>
              Current Capacity: <input type = "number" v-model ="currentcapacity" placeholder = "Current Capacity"> <br><br>
              Start Date: <input type = "datetime-local" v-model ="startdate" placeholder = "Start Date"> <br><br>
              End Date: <input type = "datetime-local" v-model ="enddate" placeholder = "End Date"> <br><br>
              Enrolment Start Date: <input type = "datetime-local" v-model ="enrolstartdate" placeholder = "Enrolment Start Date"> <br><br>
              Enrolment End Date: <input type = "datetime-local" v-model ="enrolenddate" placeholder = "Enrolment End Date"> <br><br>
              <button><input type = "submit" name="submit"></button>
          </form>
          <!-- End of form -->  
        </div>
      </div>
    </div>

  </div>
    
</template>

<script>

export default{
    name: 'createclass',
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
        console.log("Class created and updated to database!")
      }
    }
    
}

</script>

<style>
@import "../assets/style/style.css";
</style>
