type SessionT = string;
type AuthT = {
  username: string;
  password: string;
};
type gradeT = "admin" | "guest";
type UserDBT = Map<AuthT, gradeT>;
