import React from "react";

import { Point as GamePoint } from "@puzzled/types";

import { GameToScreenMapperProvider } from "@/hooks/useGameToScrenMapper.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import styles from "./Board.module.scss";

interface Props {
	className?: string;
	size: GamePoint;
	children: React.ReactNode;
}

const padding = 200;

const xVector = new ScreenPoint(45, -34);
const yVector = new ScreenPoint(45, 34);
const baseVector = new ScreenPoint(padding, padding);

const baseMapper = (
	(point: GamePoint): ScreenPoint => baseVector.add(xVector.scale(point.x)).add(yVector.scale(point.y))
);

export const Board = (props: Props) => {
	const ref = React.useRef<HTMLDivElement>(null);
	const [size, setSize] = React.useState<ScreenPoint>(new ScreenPoint(0, 0));
	const [panning, setPanning] = React.useState(false);
	const [translation, setTranslation] = React.useState(new ScreenPoint(0, 0));

	React.useLayoutEffect(() => {
		if (ref.current !== null) {
			setSize(new ScreenPoint(ref.current.offsetWidth, ref.current.offsetHeight));
		}
	}, [ref.current]);

	React.useEffect(() => {
		const observer = new ResizeObserver((entries) => {
			for (const entry of entries) {
				setSize(new ScreenPoint(entry.contentRect.width, entry.contentRect.height));
			}
		});

		if (ref.current !== null) {
			observer.observe(ref.current);
		}

		return () => {
			observer.disconnect();
		};
	}, [ref.current]);

	React.useEffect(() => {
		if (panning) {
			const onWindowMouseMove = (event: MouseEvent) => {
				if ((event.buttons & 1) === 0) {
					setPanning(false);
					return;
				}

				setTranslation((t) => {
					let newTranslation = t.add(new ScreenPoint(event.movementX, event.movementY));

					if (newTranslation.x > 0) {
						newTranslation = new ScreenPoint(0, newTranslation.y);
					}

					if (newTranslation.y > 0) {
						newTranslation = new ScreenPoint(newTranslation.x, 0);
					}

					if (newTranslation.x < size.x - width) {
						newTranslation = new ScreenPoint(size.x - width, newTranslation.y);
					}

					if (newTranslation.y < size.y - height) {
						newTranslation = new ScreenPoint(newTranslation.x, size.y - height);
					}

					return newTranslation;
				});
			};

			const onWindowMouseUp = () => {
				setPanning(false);
			};

			window.addEventListener("mousemove", onWindowMouseMove);
			window.addEventListener("mouseup", onWindowMouseUp);

			return () => {
				window.removeEventListener("mousemove", onWindowMouseMove);
				window.removeEventListener("mouseup", onWindowMouseUp);
			};
		}
	}, [panning, size]);

	const corners = [
		new GamePoint(0, 0),
		new GamePoint(props.size.x, 0),
		new GamePoint(props.size.x, props.size.y),
		new GamePoint(0, props.size.y),
	];

	const mappedCorners = corners.map(baseMapper);

	let topLeft = mappedCorners[0];
	let bottomRight = mappedCorners[0];

	for (const corner of mappedCorners) {
		if (corner.x < topLeft.x) {
			topLeft = new ScreenPoint(corner.x, topLeft.y);
		}
		if (corner.x > bottomRight.x) {
			bottomRight = new ScreenPoint(corner.x, bottomRight.y);
		}
		if (corner.y < topLeft.y) {
			topLeft = new ScreenPoint(topLeft.x, corner.y);
		}
		if (corner.y > bottomRight.y) {
			bottomRight = new ScreenPoint(bottomRight.x, corner.y);
		}
	}

	const activeWidth = bottomRight.x - topLeft.x;
	const activeHeight = bottomRight.y - topLeft.y;

	const width = activeWidth + padding * 2;
	const height = activeHeight + padding * 2;

	const baseTranslation = mappedCorners[0].subtract(topLeft);
	const mapper = (point: GamePoint) => baseMapper(point).add(baseTranslation);

	const foregroundCorners = [
		new GamePoint(-0.5, -0.5),
		new GamePoint(props.size.x - 0.5, -0.5),
		new GamePoint(props.size.x - 0.5, props.size.y - 0.5),
		new GamePoint(-0.5, props.size.y - 0.5),
	];

	const mappedForegroundCorners = foregroundCorners.map(mapper);

	return (
		<div ref={ref} className={classes(styles.board, props.className)}>
			<div
				className={classes(styles.container)}
				style={{
					transform: `translate(${translation.x}px, ${translation.y}px)`
				}}
				onMouseDown={() => setPanning(true)}
			>
				<div
					className={styles.background}
					style={{
						width,
						height,
						backgroundPosition: `${baseTranslation.x + padding}px ${baseTranslation.y + padding}px`,
					}}
				/>
				<div
					className={styles.foreground}
					style={{
						width,
						height,
						clipPath: `polygon(
							${mappedForegroundCorners[0].x}px ${mappedForegroundCorners[0].y}px,
							${mappedForegroundCorners[1].x}px ${mappedForegroundCorners[1].y}px,
							${mappedForegroundCorners[2].x}px ${mappedForegroundCorners[2].y}px,
							${mappedForegroundCorners[3].x}px ${mappedForegroundCorners[3].y}px
						)`,
						backgroundPosition: `${baseTranslation.x + padding}px ${baseTranslation.y + padding}px`,
					}}
				/>
				<GameToScreenMapperProvider mapper={mapper}>
					<div className={styles.content}>
						{props.children}
					</div>
				</GameToScreenMapperProvider>
			</div>
		</div>
	);
};
