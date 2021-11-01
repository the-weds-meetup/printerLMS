<template>
  <form>
    <div v-if="questionIndex < questions.length">
      <label>{{ question.question }}</label>
      <div v-for="c of question.choices" :key="c">
        <input type="radio" name="choice" v-model="answer" :value="c" />
        {{ c }}
      </div>
    </div>
    <div v-else>
      <button type="button" @click="restart">restart</button>
    </div>
    <button type="button" @click="submit">check</button>
  </form>
  <p>score: {{ score }}</p>
</template>

<script>
const questions = [
  {
    question: "What is American football called in England?",
    choices: ["American football", "football", "Handball"],
    rightAnswer: "American football",
  },
  {
    question: "What is the largest country in the world?",
    choices: ["Russia", "Canada", "United States"],
    rightAnswer: "Russia",
  },
  {
    question: "What is the 100th digit of Pi?",
    choices: [9, 4, 7],
    rightAnswer: 9,
  },
];
export default {
  name: 'Quiz',
  data() {
    return {
      questions,
      score: 0,
      questionIndex: 0,
      question: questions[0],
      answer: "",
    };
  },
  methods: {
    submit() {
      const { answer, question, questions, questionIndex } = this;
      if (answer === question.rightAnswer) {
        this.score++;
      }

      if (questionIndex < questions.length) {
        this.questionIndex++;
        this.question = { ...questions[this.questionIndex] };
      }
    },
    restart() {
      this.question = questions[0];
      this.answer = "";
      this.questionIndex = 0;
      this.score = 0;
    },
  },
};
</script>