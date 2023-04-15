import { useQuery } from "@apollo/client";
import React from "react";
import { useNavigate } from "react-router";

import { gql } from "@/utils/gql";

interface Props {
	children: React.ReactNode;
	fallback: string;
}

export const EnsureAdmin = (props: Props) => {
	const navigate = useNavigate();

	interface SelfResult {
		self: {
			id: string;
			name: string;
		} | null;
	}

	const { data, error } = useQuery<SelfResult>(gql`
		query SelfQuery {
			self {
				id
				name
			}
		}
	`);

	if (error || data?.self?.name !== "admin") {
		navigate(props.fallback);
		return null;
	}

	return <>{props.children}</>;
};
