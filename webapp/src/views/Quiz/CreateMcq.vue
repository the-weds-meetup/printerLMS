<template>

    <div class="container">
  
        <!-- Start -> Preview of quiz format -->
        <h1>Preview of MCQ or True/False quiz format</h1><br>

        <h2>Question - MCQ</h2><br>

        <div v-if="question.length >0">{{count}}. {{question}}</div>

        <span v-if="option1.length > 0">
            <label for="option1"><input name="answers" type="radio" :value="option1"> {{option1}}</label><br>
        </span>
        
        <span v-if="option2.length > 0">
            <label for="option2"><input name="answers" type="radio" :value="option2"> {{option2}}</label><br>
        </span>

        <span v-if="option3.length > 0">
            <label for="option3"><input name="answers" type="radio" :value="option3"> {{option3}}</label><br>
        </span>

        <span v-if="option4.length > 0">
            <label for="option4"><input name="answers" type="radio" :value="option4"> {{option4}}</label><br>
            </span>
            
      <!-- End -> Preview of quiz format -->
      <hr>
  
      <h1 class="text-center bg-primary text-white" style="border-radius:10px">Create Quiz</h1>
  
      <!-- Start of form -->
  
      <form @submit="onSubmit">
  
        <!-- Start of mcq quiz format-->
        <br>
        <label for="question">Question: 
        <textarea cols="30" rows="3" v-model="question" id="question"></textarea>
        </label><br><br>

        <label for="option1">Option 1:
        <input type="text" v-model="option1">
        </label>

        <label class="option2" for="option2">Option 2:
        <input type="text" v-model="option2">
        </label><br><br>

        <label for="option2">Option 3:
        <input type="text" v-model="option3">
        </label>

        <label class="option4" for="option2">Option 4:
        <input type="text" v-model="option4">
        </label><br><br>

        <label class="answer" for="answer">Answer:
        <input type="text" v-model="answer">
        </label><br><br>

        <button class="btn btn-primary submit" type = "button">
        Add Quiz
        </button>

        <!-- Button to toggle between mcq and true/false -->
        <button type="button" class="btn btn-dark toggle" v-on:click="this.$router.push('/quiz/createtf')"> 
          Toggle between MCQ and true/false
        </button>
  
        <!-- End of mcq quiz format -->
      
      </form>
      <!-- End of form -->
  
    </div>
  
  </template>
  
  
  <script>
  
  export default {
    name: 'Createmcq',
    data(){
      return{
        count: '1',
        question: '',
        option1: '',
        option2: '',
        option3: '',
        option4: '',
        answer: ''
      }
    }
  };
      
  </script>
  
    <style>
    button.submit{
    position: relative;
    left: 180px;
    }

    button.toggle{
    position: relative;
    left: 350px;
    bottom: 265px;
    }

    .option2{
    position:relative; left:10px;
    }
    .option4{
    position:relative; left:10px;
    }

    .answer{
    position:relative; left:10px;
    }

  
  </style>
    