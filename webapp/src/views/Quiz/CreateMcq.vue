<template>
  <div class="container">
    <!-- Start -> Preview of quiz format -->
    <h1>Preview of MCQ or True/False quiz format</h1>
    <br />

    <h2>Question - MCQ</h2>
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

    <span v-if="option3.length > 0">
      <label for="option3"
        ><input name="answers" type="radio" :value="option3" />
        {{ option3 }}</label
      ><br />
    </span>

    <span v-if="option4.length > 0">
      <label for="option4"
        ><input name="answers" type="radio" :value="option4" />
        {{ option4 }}</label
      ><br />
    </span>

    <!-- End -> Preview of quiz format -->
    <hr />

    <h1 class="text-center bg-primary text-white" style="border-radius: 10px">
      Create Quiz
    </h1>

    <!-- Start of form -->

    <form @submit.prevent="onSubmit()">
      <!-- Start of mcq quiz format-->
      <br />
      <label for="question"
        >Question:
        <textarea
          id="question"
          v-model="question"
          cols="30"
          rows="3"
        ></textarea></label
      ><br /><br />

      <label for="option1"
        >Option 1:
        <input v-model="option1" type="text" />
      </label>

      <label class="option2" for="option2"
        >Option 2: <input v-model="option2" type="text" /> </label
      ><br /><br />

      <label for="option3"
        >Option 3:
        <input v-model="option3" type="text" />
      </label>

      <label class="option4" for="option2"
        >Option 4: <input v-model="option4" type="text" /> </label
      ><br /><br />

      <label class="answer" for="answer"
        >Answer: <input v-model="answer" type="text" /> </label
      ><br /><br />

      <button class="btn btn-primary submit" type="submit">Add Quiz</button>

      <!-- Button to toggle between mcq and true/false -->
      <button
        type="button"
        class="btn btn-dark toggle"
        @click="$router.push('/quiz/createtf')"
      >
        Toggle between MCQ and true/false
      </button>

      <!-- End of mcq quiz format -->
    </form>
    <!-- End of form -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Createmcq',
  data() {
    return {
      count: '1',
      question: '',
      option1: '',
      option2: '',
      option3: '',
      option4: '',
      answer: '',
    };
  },
  methods: {
    onSubmit() {
      choices = this.choice.append(option1);
      choices = this.choice.append(option2);
      choices = this.choice.append(option3);
      choices = this.choice.append(option4);
      axios
        .post(process.env.VUE_APP_BACKEND + '/api/quiz/add', {
          question: this.question,
          choices: this.choices,
          answer: this.answer,
        })
        .then(() => {
          this.$router.push('/quiz/createmcq');
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

.option2 {
  position: relative;
  left: 10px;
}
.option4 {
  position: relative;
  left: 10px;
}

.answer {
  position: relative;
  left: 10px;
}
</style>
