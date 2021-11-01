<template>

  <div class="container">

    <!-- Start -> Preview of quiz format -->
    <h1>Preview of MCQ or True/False quiz format</h1>

    <div v-if ="mcq">

      <h2>Question - MCQ</h2>

      <div>{{question}}</div>
      <label for="option1"><input name="answers" type="radio" :value="option1"> {{option1}}</label><br>
      <label for="option2"><input name="answers" type="radio" :value="option2"> {{option2}}</label><br>
      <label for="option3"><input name="answers" type="radio" :value="option3"> {{option3}}</label><br>
      <label for="option4"><input name="answers" type="radio" :value="option4"> {{option4}}</label><br>
    </div>

    <div v-if ="!mcq">

      <h2>Question - True/False</h2>

      <div>{{question}}</div>
      <label for="option1"><input name="answers" type="radio" :value="option1"> {{option1}}</label><br>
      <label for="option2"><input name="answers" type="radio" :value="option2"> {{option2}}</label><br>
    </div>
    <!-- End -> Preview of quiz format -->
    <hr>

    <h1 class="text-center bg-primary text-white" style="border-radius:10px">Create Quiz</h1>

    <!-- Start of form -->

    <form @submit="onSubmit">

      <!-- Button to toggle between mcq and true/false -->
      <button type="button" class="btn btn-dark toggle" v-on:click="mcq =!mcq"> 
        Toggle between MCQ and true/false
      </button>

      <!-- Start of mcq quiz format-->
      <div v-if="mcq">

        <label for="question">Question: 
          <textarea cols="30" rows="3" v-model="question" id="question"></textarea>
        </label><br><br>

        <label for="option1">Option 1
          <input type="text" v-model="option1">
        </label><br><br>

        <label for="option2">Option 2
          <input type="text" v-model="option2">
        </label><br><br>

        <label for="option2">Option 3
          <input type="text" v-model="option3">
        </label><br><br>

        <label for="option2">Option 4
          <input type="text" v-model="option4">
        </label><br><br>

         <label for="answer">Answer
          <input type="text" v-model="answer">
        </label><br><br>

        <button class="btn btn-primary submit" type = "button">
          Add Quiz
        </button>

      </div>

      <!-- End of mcq quiz format -->

      <!-- Start of true/false format -->

      <div v-if="!mcq">

        <label for="question">Question: 
          <textarea cols="30" rows="3" v-model="question" id="question"></textarea>
        </label><br><br>

        <label for="option1">Option 1
          <input type="text" v-model="option1">
        </label><br><br>

        <label for="option2">Option 2
          <input type="text" v-model="option2">
        </label><br><br>

        <label for="answer">Answer
          <input type="text" v-model="answer">
        </label><br><br>

        <button class="btn btn-primary submit" type = "button">
          Add Quiz
        </button>

      </div>

      <!-- End of true/false format -->
    
    </form>
    <!-- End of form -->

  </div>

</template>


<script>

export default {
  name: 'Createquiz',
  data(){
    return{
      mcq: true,
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
  left: 450px;
  top: 35px;
}

</style>
  