<template>

<div class = "container">
  <form>
  <br>
    <div v-if="questionIndex < questions.length">
      <label>{{count + ". " + question.question}}</label>
      <br>
      <div v-for="choice of question.choices" :key="choice">
        <input type="radio" name="choice" v-model="answer" :value="choice" required/>
        {{ choice }}
      </div><br>
      <button type="button" class="btn btn-info" @click="verify">Submit</button>
      <button type="button" class="btn btn-danger verify" @click="submit">Next</button><br><br>
      <div id="message"></div>
      <p>score: {{score}}  </p>
      
    </div>
    <div v-else>
      <br>
      <button type="button" class="btn btn-warning" @click="restart">Restart</button><br><br>
      <p>score: {{ score + " out of " + total_score}}  </p>
    </div><br>
    
  </form><br>
  
</div>

</template>

<style>
button.verify{
  position: relative;
  left: 10px;
}

</style>

<script>
const questions = [
  {
    question: "Short form for Singapore",
    choices: ["SG", "MY", "HA", "FR"],
    rightAnswer: "SG",
  },
  {
    question: "The Great Wall of China is longer than the distance between London and Beijing.",
    choices: ["True","False"],
    rightAnswer: "True",
  },
  {
    question: "What is the largest country in the world?",
    choices: ["Russia", "Canada", "United States"],
    rightAnswer: "Russia",
  },
  {
    question: "There are 219 episodes of Friends.",
    choices: ["True","False"],
    rightAnswer: "False",
  },
];
export default {
  name: 'Quiz',
  data() {
    return {
      count:1,
      questions,
      score: 0,
      questionIndex: 0,
      question: questions[0],
      answer: "",
      total_score:0,
    };
  },
  methods: {
    submit(){
      const { answer, question, questions, questionIndex } = this;
    
      if (questionIndex < questions.length) {
        this.questionIndex++;
        this.question = { ...questions[this.questionIndex] };
        document.getElementById("message").innerHTML="";
      }

      this.count+= 1
      this.total_score += 1
    },
    verify(){
      console.log("here");
      if(this.answer === this.question.rightAnswer){
        this.score++;
        document.getElementById("message").innerHTML="You are correct!";
      }
      else{
        document.getElementById("message").innerHTML="You are wrong! Correct answer: "+ this.question.rightAnswer+".";
      }
    },
    restart() {
      this.question = questions[0];
      this.answer = "";
      this.questionIndex = 0;
      this.score = 0;
      this.count = 1;
      this.total_score = 0;
    },
  },
};
</script>
