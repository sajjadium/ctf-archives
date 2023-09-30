export type Question = {
    question: string,
    answers: string[],
    image: string
}

export type GameState = {
    question: Question,
    questionIndex: number,
    scoreboard: Record<string, number>,
    correctAnswer: number | undefined,
    timeLeft: number,
}