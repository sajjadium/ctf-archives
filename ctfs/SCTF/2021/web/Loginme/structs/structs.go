package structs

type UserInfo struct {
	Id       int
	Username string
	Age      string
	Password string
}

var Users = []UserInfo{
	{
		Id:       1,
		Username: "Grandpa Lu",
		Age:      "22",
		Password: "hack you!",
	},
	{
		Id:       2,
		Username: "Longlone",
		Age:      "??",
		Password: "i don't know",
	},
	{
		Id:       3,
		Username: "Teacher Ma",
		Age:      "20",
		Password: "guess",
	},
}

var Admin = UserInfo{
	Id:       0,
	Username: "Admin",
	Age:      "",
	Password: "flag{}",
}
