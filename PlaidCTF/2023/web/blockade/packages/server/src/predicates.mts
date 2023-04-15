import { Raw } from "typeorm";

import { Point } from "@puzzled/types";

export const EqualsPoint = (
	(location: Point) =>
		Raw((alias) => `${alias} ~= (:location)::point`, { location: location.toPostgres() })
);

export const Distance = (
	(location: Point) =>
		Raw((alias) => `${alias} <-> (:location)::point`, { location: location.toPostgres() })
);

export const DistanceLessThanOrEqualTo = (
	(location: Point, distance: number) =>
		Raw((alias) => `${alias} <-> (:location)::point <= :distance`, { location: location.toPostgres(), distance })
);

export const DistanceGreaterThanOrEqualTo = (
	(location: Point, distance: number) =>
		Raw((alias) => `${alias} <-> (:location)::point >= :distance`, { location: location.toPostgres(), distance })
);

export const HorizontallyAlignedWith = (
	(location: Point) =>
		Raw((alias) => `${alias} ?- (:location)::point`, { location: location.toPostgres() })
);

export const VerticallyAlignedWith = (
	(location: Point) =>
		Raw((alias) => `${alias} ?| (:location)::point`, { location: location.toPostgres() })
);

export const StrictlyLeftOf = (
	(location: Point) =>
		Raw((alias) => `${alias} << (:location)::point`, { location: location.toPostgres() })
);

export const StrictlyRightOf = (
	(location: Point) =>
		Raw((alias) => `${alias} >> (:location)::point`, { location: location.toPostgres() })
);

export const StrictlyAbove = (
	(location: Point) => // note: y-axis is inverted
		Raw((alias) => `${alias} <<| (:location)::point`, { location: location.toPostgres() })
);

export const StrictlyBelow = (
	(location: Point) => // note: y-axis is inverted
		Raw((alias) => `${alias} |>> (:location)::point`, { location: location.toPostgres() })
);
