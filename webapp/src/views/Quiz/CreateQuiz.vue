<template>

  <div class="container">

    <h1>Preview of MCQ or True/False quiz format</h1>
    <h2>Question</h2>

    <div>{{question}}</div>
    <label for="option1"><input name="answers" type="radio" :value="option1"> {{option1}}</label><br>
    <label for="option2"><input name="answers" type="radio" :value="option2"> {{option2}}</label><br>
    <label for="option2"><input name="answers" type="radio" :value="option3"> {{option3}}</label><br>
    <label for="option2"><input name="answers" type="radio" :value="option4"> {{option4}}</label><br>
    
    <hr>

    <h2>Create your multiple-choice question here</h2>

    <label for="question">Question: 
      <input type = "text" v-model="question" id="question" cols="30" rows="3">
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

    <button class="btn btn-primary submit" type = "button">Submit</button>

  </div>

</template>


<script>

export default {
  name: 'Createquiz',
  data(){
    return{
      question: '',
      option1: '',
      option2: '',
      option3: '',
      option4: ''
    }
  }
};
    
</script>

<style>
button.submit{
  position: relative;
  left: 180px;
}

</style>
  