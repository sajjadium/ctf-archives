let sbxed = await (async _=>{
	let lib = Deno.dlopen( "/lib/x86_64-linux-gnu/libc.so.6",{
		close: { parameters: ["i32"], result: "i32"},
		setuid: { parameters: ["i32"], result: "i32"},
		setgid: { parameters: ["i32"], result: "i32"}
	});
	let syms = lib.symbols;

	if(
		!syms.setgid(1337) &&
		!syms.setuid(1337) &&
		!syms.close(0) &&
		!syms.close(1) &&
		!syms.close(2)
	){
		lib.close();
		await Deno.permissions.revoke({name:'ffi'});
		return true;
	}
	return false;
})()

if(sbxed){
	eval(atob(Deno.args[0]).slice(0,100))
}

