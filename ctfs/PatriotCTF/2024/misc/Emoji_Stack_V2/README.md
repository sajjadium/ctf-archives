Back by popular demand, V2 of EmojiStack is ready to release! Following user feedback, we've made some changes to how things work:

It was pointed out that EmojiStack wasn't actually turing complete, and was instead just "A really dumb markup language." To remedy this, we've added three new commands for execution control, please see details below. Sticking with our philosophy of readability, we figured that hex numbers are too complicated and have decided to switch to easily read emoji representations. Numbers will now be encoded in base 12 from 🕛 to 🕚. Example: 🔁5f --> 🔁🕛🕖🕚 For our second release, it only seemed fair to add a second stack dimension! Emoji Stack now supports a 255x255 grid of cells. With the addition of two dimensional stacks, a good idea fairy said it might be cool to represent stack states using images. The state of the stack is now saved as a 255x255 8 bit grey scale image to allow for the pre-initialization of the stack. Images are stored raster-scan order with 0,0 being the top left of the image.

Commands

    👉: Move the stack pointer one cell to the right
    👈: Move the stack pointer one cell to the left
    👆: Move the stack pointer one cell upwards
    👇: Move the stack pointer one cell downwards
    👍: Increment the current cell by one, bounded by 255
    👎: Decrement the current cell by one, bounded by 0
    💬: Print the ASCII value of the current cell
    👂: Read one character of ASCII and store it in the current cell
    🫸: If the current cell is zero, jump to the next instruction after the respective 🫷
    🫷: If the current cell is non-zero, jump back to the respective 🫸
    🔁###: Repeat the previous instruction ## times

Author: CACI
