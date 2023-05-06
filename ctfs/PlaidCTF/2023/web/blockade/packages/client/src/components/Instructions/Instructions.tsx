import Instr1 from "@assets/instr-1.png";
import Instr2 from "@assets/instr-2.png";
import React from "react";

import { Heading } from "@puzzled/types";

import { BrigFrames, BrigHaloSpritesheet, BrigSpritesheet } from "@/spritesheets/Brig.js";
import { BuoyFrames, BuoySpritesheet } from "@/spritesheets/Buoy.js";
import { FrigateFrames, FrigateHaloSpritesheet, FrigateSpritesheet } from "@/spritesheets/Frigate.js";
import { GalleonFrames, GalleonHaloSpritesheet, GalleonSpritesheet } from "@/spritesheets/Galleon.js";
import { SloopFrames,SloopHaloSpritesheet,SloopSpritesheet } from "@/spritesheets/Sloop.js";
import { ScreenPoint } from "@/types/ScreenPoint.js";
import { classes } from "@/utils/css.js";

import { Button } from "../Button/Button.js";
import { OutlineText } from "../OutlineText/OutlineText.js";
import { Sprite } from "../Sprite/Sprite.js";

import styles from "./Instructions.module.scss";

interface Props {
	onClose: () => void;
}

export const Instructions = (props: Props) => (
	<div className={styles.instructionsContainer}>
		<div className={styles.instructions}>
			<div className={styles.title}>Blockade!</div>
			<div className={classes(styles.section, styles.youControl)}>
				<div className={styles.text}>
					You control the ships outlined in <OutlineText>blue</OutlineText>!
				</div>
				<div className={styles.images}>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={SloopHaloSpritesheet}
							frame={SloopFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={SloopSpritesheet}
							frame={SloopFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={BrigHaloSpritesheet}
							frame={BrigFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={BrigSpritesheet}
							frame={BrigFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={GalleonHaloSpritesheet}
							frame={GalleonFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={GalleonSpritesheet}
							frame={GalleonFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={FrigateHaloSpritesheet}
							frame={FrigateFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={FrigateSpritesheet}
							frame={FrigateFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
				</div>
			</div>
			<div className={classes(styles.section, styles.enemyControl)}>
				<div className={styles.images}>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={SloopHaloSpritesheet}
							frame={SloopFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={SloopSpritesheet}
							frame={SloopFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={BrigHaloSpritesheet}
							frame={BrigFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={BrigSpritesheet}
							frame={BrigFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={GalleonHaloSpritesheet}
							frame={GalleonFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={GalleonSpritesheet}
							frame={GalleonFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.halo}
							mask
							spritesheet={FrigateHaloSpritesheet}
							frame={FrigateFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
						<Sprite
							spritesheet={FrigateSpritesheet}
							frame={FrigateFrames[Heading.South]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
				</div>
				<div className={styles.text}>
					Your enemies control the ships outlined in <OutlineText>red</OutlineText>!
				</div>
			</div>
			<div className={classes(styles.section, styles.moveAndFire)}>
				<div className={styles.text}>
					Move your ships and fire your cannons to sink your enemies!
				</div>
				<div className={styles.images}>
					<img className={styles.image} src={Instr1} />
				</div>
			</div>
			<div className={classes(styles.section, styles.hazards)}>
				<div className={styles.images}>
					<img className={styles.image} src={Instr2} />
				</div>
				<div className={styles.text}>
					Be careful of gusts, whirlpools, and rocks!
				</div>
			</div>
			<div className={classes(styles.section, styles.buoys)}>
				<div className={styles.text}>
					Move so that buoys are within the influence range of your ships to score points!  Buoys are worth 1,
					2, or 3 points each, and score double the first turn they are within your influence.  Keep your
					enemies away from the buoys to maximize your score!
				</div>
				<div className={styles.images}>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.sprite}
							spritesheet={BuoySpritesheet}
							frame={BuoyFrames[1]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.sprite}
							spritesheet={BuoySpritesheet}
							frame={BuoyFrames[2]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
					<div className={styles.spriteContainer}>
						<Sprite
							className={styles.sprite}
							spritesheet={BuoySpritesheet}
							frame={BuoyFrames[3]}
							offset={new ScreenPoint(50, 50)}
						/>
					</div>
				</div>
			</div>
			<Button
				className={styles.close}
				onClick={props.onClose}
			>
				Yaarrr!
			</Button>
		</div>
	</div>
);
