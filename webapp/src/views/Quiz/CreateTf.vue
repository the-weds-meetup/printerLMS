<template>
  <div class="container">
    <!-- Start -> Preview of quiz format -->
    <h1>Preview of MCQ or True/False quiz format</h1>
    <br />

    <h2>Question - True/False</h2>
    <br />

    <div v-if="question.length > 0">{{ count }}. {{ question }}</div>

    <span v-if="option1.length > 0">
      <label for="option1"
        ><input name="answers" type="radio" :value="option1" />
        {{ option1 }}</label
      ><br />
    </span>

    <span v-if="option2.length > 0">
      <label for="option2"
        ><input name="answers" type="radio" :value="option2" />
        {{ option2 }}</label
      ><br />
    </span>

    <!-- End -> Preview of quiz format -->
    <hr />

    <h1 class="text-center bg-primary text-white" style="border-radius: 10px">
      Create Quiz
    </h1>

    <!-- Start of form -->

    <form @submit.prevent="onSubmit()">
      <!-- Start of true/false format -->

      <br />
      <label for="question"
        >Question:
        <textarea
          cols="30"
          rows="3"
          v-model="question"
          id="question"
        ></textarea></label
      ><br /><br />

      <label for="option1"
        >Option 1:
        <input type="text" v-model="option1" /> </label
      ><br /><br />

      <label for="option2"
        >Option 2:
        <input type="text" v-model="option2" /> </label
      ><br /><br />

      <label class="answer" for="answer"
        >Answer:
        <input type="text" v-model="answer" /> </label
      ><br /><br />

      <button class="btn btn-primary submit" type="submit">Add Quiz</button>

      <!-- Button to toggle between mcq and true/false -->
      <button
        type="button"
        class="btn btn-dark toggle"
        v-on:click="this.$router.push('/quiz/createmcq')"
      >
        Toggle between MCQ and true/false
      </button>

      <!-- End of true/false format -->
    </form>
    <!-- End of form -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Createtf',
  data() {
    return {
      count: '1',
      question: '',
      option1: '',
      option2: '',
      answer: '',
      choices: [],
    };
  },
  methods: {
    onSubmit() {
      /* console.log("Class created and updated to database!") */
      console.log('reached here');
      console.log(option1);
      console.log(option2);
      console.log(choices);
      choices = this.choice.append(option1);
      choices = this.choice.append(option2);
      axios
        .post('/api/quiz/add', {
          question: this.question,
          choices: this.choices,
          answer: this.answer,
        })
        .then(() => {
          console.log(choices);
          this.$router.push('/quiz/createtf');
        })
        .catch((error) => {
          alert(error.response.data.message);
          this.error = error.response.data.message;
        });
    },
  },
};
</script>

<style>
button.submit {
  position: relative;
  left: 170px;
}

button.toggle {
  position: relative;
  left: 350px;
  bottom: 265px;
}

.answer {
  position: relative;
  left: 10px;
}
</style>
