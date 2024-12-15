$("#run").on("click", () => tryCatch(run));

const run: Function = async () => {

  let selections = [
    "3_0",
    "1_2",
    "3_2",
    "1_1",
    "5_0",
    "0_0",
    "2_0",
    "1_0",
    "3_1",
    "5_2",
    "5_1",
    "6_0",
    "6_1",
    "3_3",
    "2_1",
    "2_2",
    "0_1"
  ];

  await PowerPoint.run(async (context) => {
    var correct = 1;

    for (let i = 0; i < selections.length; i++) {
      const shapes: PowerPoint.ShapeCollection = context.presentation.slides.getItemAt(
        Number.parseInt(selections[i][0])
      ).shapes;

      let shape: PowerPoint.Shape;

      if (selections[i][0] != "0") {
        shape = shapes.getItemAt(1);
      } else {
        shape = shapes.getItemAt(0);
      }

      const textFrame: PowerPoint.TextFrame = shape.textFrame.load("textRange");
      await context.sync();
      const text = textFrame.textRange.text;
      await context.sync();

      switch (selections[i][0]) {
        case "0":
          switch (selections[i][2]) {
            case "0":
              if (text[0] != String.fromCharCode(123)) {
                correct = 0;
              }
              break;
            case "1":
              if (text[23] != String.fromCharCode(125)) {
                correct = 0;
              }
              break;
          }
          break;

        case "1":
          switch (selections[i][2]) {
            case "0":
              if (text[41] != String.fromCharCode(80)) {
                correct = 0;
              }
              break;
            case "1":
              if (text[138] != String.fromCharCode(67)) {
                correct = 0;
              }
              break;
            case "2":
              if (text[184] != String.fromCharCode(72)) {
                correct = 0;
              }
              break;
          }
          break;

        case "2":
          switch (selections[i][2]) {
            case "0":
              if (text[0] != String.fromCharCode(80)) {
                correct = 0;
              }
              break;
            case "1":
              if (text[83] != String.fromCharCode(101))
              {
                correct = 0;
              }
              break;
            case "2":
              if (text[179] != String.fromCharCode(82)) {
                correct = 0;
              }
              break;
          }
          break;

        case "3":
          switch (selections[i][2]) {
            case "0":
              if (text[25] != String.fromCharCode(78)) {
                correct = 0;
              }
              break;
            case "1":
              if (text[26] != String.fromCharCode(84)) {
                correct = 0;
              }
              break;
            case "2":
              if (text[28] != String.fromCharCode(52)) {
                correct = 0;
              }
              break;
            case "3":
              if (text[84] != String.fromCharCode(84)) {
                correct = 0;
              }
              break;
          }
          break;

        case "5":
          switch (selections[i][2]) {
            case "0":
              if (text[105] != String.fromCharCode(75)) {
                correct = 0;
              }
              break;
            case "1":
              if (text[106] != String.fromCharCode(109)) {
                correct = 0;
              }
              break;
            case "2":
              if (text[219] != String.fromCharCode(88)) {
                correct = 0;
              }
              break;
          }
          break;

        case "6":
          switch (selections[i][2]) {
            case "0":
              if (text[52] != String.fromCharCode(52)) {
                correct = 0;
              }
              break;

            case "1":
              if (text[95] != String.fromCharCode(53)) {
                correct = 0;
              }
              break;
          }
          break;
      }
    }
    if (correct) {
      console.log("Thanx for helping me out, now go input the flag");
    } else {
      console.log("I don't think i had that in mind");
    }
  });
};

const tryCatch: (callback: Function) => void = async (callback: Function) => {
  try {
    await callback();
  } catch (error) {
    console.error(error);
  }
};
