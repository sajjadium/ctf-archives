import { useQuery } from "@apollo/client";
import React from "react";
import { Link, NavLink } from "react-router-dom";

import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";

import styles from "./Header.module.scss";

interface Props {
	className?: string;
}

export const Header = (props: Props) => {
	interface SelfResult {
		self: {
			id: string;
			name: string;
		}
	}

	const { data } = useQuery<SelfResult>(gql`
		query SelfQuery {
			self {
				id
				name
			}
		}
	`, {
		errorPolicy: "ignore"
	});

	let content = (
		<>
			<Link className={styles.link} to="/login">Log-In</Link>
			{" | "}
			<Link className={styles.link} to="/register">Register</Link>
		</>
	);

	if (data?.self) {
		content = (
			<>
				{"Hello, "}
				<Link className={styles.link} to={`/user/${data.self.id}`}>{data.self.name}</Link>
				{" | "}
				<Link className={styles.link} to="/show/create">Add Show</Link>
				{" | "}
				<Link className={styles.link} to="/episode/create">Add Episode</Link>
				{" | "}
				<Link className={styles.link} to="/playlist/create">Create Playlist</Link>
				{" | "}
				<div
					className={styles.link}
					onClick={() => {
						localStorage.removeItem("token");
						window.location.reload(); // hard reload
					}}
				>
					Log-Out
				</div>
			</>
		);
	}

	return (
		<header className={classes(styles.header, props.className)}>
			<div className={styles.top}>
				<Link className={styles.link} to="/">Home</Link>
				{" | "}
				{content}
			</div>
			<div className={styles.middle}>
				<h1 className={styles.title}>Davy Jones' Putlocker</h1>
			</div>
			<div className={styles.bottom}>
				<NavLink
					className={({ isActive }) => classes(styles.link, isActive ? styles.active : undefined)}
					to="/"
				>
					Home
				</NavLink>
				<NavLink
					className={({ isActive }) => classes(styles.link, isActive ? styles.active : undefined)}
					to="/genre/cb233ddd-48da-4d2e-a34d-4b2a7bd856dd"
				>
					Comedy Series
				</NavLink>
				<NavLink
					className={({ isActive }) => classes(styles.link, isActive ? styles.active : undefined)}
					to="/genre/04f3fdf0-b2af-43ec-b38a-5408f9ea02a9"
				>
					Fantasy Series
				</NavLink>
			</div>
		</header>
	);
};
