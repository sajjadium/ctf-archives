import { useQuery } from "@apollo/client";
import React from "react";

import { Panel } from "@/components/Panel";
import { Rating } from "@/components/Rating";
import { classes } from "@/utils/css";
import { gql } from "@/utils/gql";
import { uuidify } from "@/utils/uuid";

import { AddToPlaylistButton } from "../AddToPlaylistButton";
import { ReportButton } from "../ReportButton";

import styles from "./EpisodePanel.module.scss";

interface Props {
	className?: string;
	id: string;
	autoplay?: boolean;
	onComplete?: () => void;
}

export const EpisodePanel = (props: Props) => {
	interface SelfResult {
		self: {
			id: string;
		};
	}

	const { data: selfData } = useQuery<SelfResult>(gql`
		query SelfQuery {
			self {
				id
			}
		}
	`);

	interface EpisodeQueryResult {
		episode?: {
			id: string;
			name: string;
			description: { __html: string };
			url: string;
			rating: number;
			ratingCount: number;
			show: {
				owner: {
					id: string;
				};
			};
		};
	}

	const { data, loading, error } = useQuery<EpisodeQueryResult>(gql`
		query EpisodeQuery {
			episode(id: ${uuidify(props.id)}) {
				id
				name
				description
				url
				rating
				ratingCount
				show {
					owner {
						id
					}
				}
			}
		}
	`);

	const [videoReady, setVideoReady] = React.useState(false);
	const videoRef = React.useRef<HTMLVideoElement>(null);

	React.useEffect(() => {
		setVideoReady(false);
	}, [data?.episode?.url]);

	React.useEffect(() => {
		const video = videoRef.current;

		if (videoReady && props.autoplay && video !== null) {
			video.play().catch(() => {
				video.muted = true;
				video.play();
			});
		}
	}, [videoReady, props.autoplay]);

	const editLink = (
		selfData?.self?.id !== undefined && selfData?.self?.id === data?.episode?.show?.owner?.id
			? (
				<a className={styles.editLink} href={`/episode/${props.id}/edit`}>(Edit)</a>
			)
			: null
	);

	return (
		<Panel
			className={classes(props.className, styles.episodePanel)}
			title={
				loading ? "Loading..." :
				data === undefined || error || data.episode === undefined ? "Error loading episode" :
				<>
					{data.episode.name}
					{editLink}
				</>
			}
		>
			{
				!loading && error === undefined && data?.episode !== undefined
					? (
						<>
							<div
								className={styles.description}
								dangerouslySetInnerHTML={data.episode.description}
							/>
							<ReportButton className={styles.report} />
							<AddToPlaylistButton
								className={styles.addToPlaylistButton}
								episode={props.id}
							/>
							<Rating
								className={styles.rating}
								episode={props.id}
							/>
							<video
								key={data.episode.id}
								ref={videoRef}
								className={styles.video}
								controls
								onEnded={props.onComplete}
								onCanPlay={() => setVideoReady(true)}
							>
								<source src={data.episode.url} type="video/mp4" />
							</video>
						</>
					)
					: null
			}
		</Panel>
	);
};
