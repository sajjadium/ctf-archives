class User {
	#name;#nickname;#images;#decade;
	constructor(name,nickname,images,decade) {
		this.#name = name;
		this.#nickname = nickname;
		this.#images = images;
		this.#decade = decade;
	}

	get name() {
		return this.#name;
	}

	get nickname() {
		return this.#nickname;
	}

	get images() {
		return this.#images;
	}

	get decade() {
		return this.#decade;
	}

	update(images) {
		this.#images = images;
	}
	
	addImage(url,description) {
		images[this.#nickname][md5(url).slice(0,6)] = [
			url,
			description,
		];
	}


	addFriend(friend) {
		if(friend instanceof User && md5(friend.nickname) != "1f4e0a21bb6eef87c17ca2abdfc28369") {
			for(let img in friend.images[friend.nickname]) {
				if(!(friend.nickname.trim() in this.images)) this.images[friend.nickname.trim()] = {};
				// console.log(this.images[friend.nickname.trim()]["test"] = 123);
				this.images[friend.nickname.trim()][img] = friend.images[friend.nickname][img];
			}
		}
	}
}