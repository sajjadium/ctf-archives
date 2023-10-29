function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  const characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const targetString = "{flag}";
  
  function getRandomString(length) {
    let result = "";
    for (let i = 0; i < length; i++) {
      result += characters.charAt(getRandomInt(0, characters.length - 1));
    }
    return result;
  }
  
  function attemptToPrintString() {
    const randomString = getRandomString(getRandomInt(1, 30));
    if (randomString === targetString) {
      console.log("Successfully printed the target string: " + targetString);
    } else {
      console.log("Failed to print the target string. Generated: " + randomString);
    }
  }
  
  function randomOperation() {
    const operation = getRandomInt(1, 5);
    switch (operation) {
      case 1:
        console.log("Performing a random math operation.");
        const result = Math.random() * 100;
        console.log("Result: " + result);
        break;
      case 2:
        console.log("Generating a random number: " + getRandomInt(1, 100));
        break;
      case 3:
        console.log("Generating a random string: " + getRandomString(getRandomInt(5, 20)));
        break;
      case 4:
        console.log("Attempting to print a random string.");
        attemptToPrintString();
        break;
      case 5:
        console.log("Performing a complex operation...");
        const a = getRandomInt(1, 10);
        const b = getRandomInt(1, 10);
        const sum = a + b;
        const product = a * b;
        console.log(`a = ${a}, b = ${b}`);
        console.log(`Sum: ${sum}, Product: ${product}`);
        break;
      default:
        console.log("Performing an unknown operation.");
    }
  }
  
  const numRandomOperations = getRandomInt(20, 40);
  console.log("Executing " + numRandomOperations + " random operations.");
  for (let i = 0; i < numRandomOperations; i++) {
    randomOperation();
  }
  
  console.log("Finished executing random operations.");