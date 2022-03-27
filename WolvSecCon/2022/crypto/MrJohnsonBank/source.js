// The authentication code is written in johnson script, a much, much slower version of JavaScript

/**
 * Checks user inputted password against a correct password
 *
 * @param {string} userInput - the password inputted by the user
 * @param {string} correctPassword - the correct password
 * @returns {boolean} - indicates whether the user's password (userInput) matches the correct password (correctPassword)
 */
function checkPassword(userInput, correctPassword){
    return userInput === correctPassword;
}
