<template>
<div class="container">
    <div class="bubbles">
        <span style="--i:5;"></span>
        <span style="--i:1;"></span>
        <span style="--i:2;"></span>
        <span style="--i:3;"></span>
        <span style="--i:4;"></span>
        <span style="--i:5;"></span>
        <span style="--i:6;"></span>
        <span style="--i:8;"></span>
        <span style="--i:5;"></span>
        <span style="--i:1;"></span>
        <span style="--i:1;"></span>
        <span style="--i:3;"></span>
        <span style="--i:5;"></span>
        <span style="--i:6;"></span>
        <span style="--i:8;"></span>
        <span style="--i:2;"></span>
        <span style="--i:6;"></span>
    </div>
</div>

</template>
  
<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
/* Reset CSS for the entire page */
html, body {
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Prevent horizontal scrolling */
  width: 100%;
  height: 100%;
}

.container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw; /* Use viewport units */
  height: 100vh;
  overflow: hidden; /* Hide overflow */
  z-index: -1; /* Keep animation behind content */
  pointer-events: none; /* Allow clicking through the animation */
}

.bubbles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  padding: 0;
  margin: 0;
  overflow: hidden;
  justify-content: space-evenly;
}

.bubbles span {
  position: relative;
  width: 1px;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.382);
  margin: 0 1px;
  border-radius: 50%;
  box-shadow: 0 0 0 10px #d9ab2358, 0 0 0 10px, 0 0 0 10px #592e2564;
  animation: animate 15s linear infinite;
  animation-duration: calc(165s/ var(--i));
}
.bubbles span:nth-child(even){
    background-color: brown;
    box-shadow: 0 0 0 10px #a64e4e, 0 0 0 10px green, 0 0 0 10px greenyellow;
}
@keyframes animate {
  0% {
    transform: translateY(100vh) scale(0);
  }
  100% {
    transform: translateY(-10%) scale(1);
  }
}
@media (max-width: 767px) {
    .bubbles span {
    /* Smaller bubbles on mobile */
    box-shadow: 0 0 0 5px #d9ab2358, 0 0 0 5px, 0 0 0 5px #592e2564;
    animation-duration: calc(120s/ var(--i));
  }
  
  .bubbles span:nth-child(even) {
    box-shadow: 0 0 0 5px #a64e4e, 0 0 0 5px green, 0 0 0 5px greenyellow;
  }
   
}
</style>