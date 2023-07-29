import Link from "next/link";

export default function NavBar() {
    return (
        <nav className="bg-[#EDE7EF] py-5 px-12 flex justify-between">
            <Link href="/">
                <p className="text-3xl font-bold">frogshare™️</p>
            </Link>
        </nav>
    );
}
