import { useMemo, memo } from "react";
import "external-svg-loader";
import { Tooltip } from "react-tooltip";
import useIsMounted from "@/hooks/useIsMounted";

const Frog = memo(({ frog }) => {
    const { isMounted } = useIsMounted();

    const { name, img, creator } = frog;

    const svgProps = useMemo(() => {
        try {
            return JSON.parse(frog.svgProps);
        } catch {
            return null;
        }
    }, [frog.svgProps]);

    if (!isMounted) return null;
    return (
        <>
            <div
                className="flex flex-col bg-white p-8 rounded-xl shadow-md text-center h-[169px] w-[169px] mr-4 mb-4 relative"
                data-tooltip-id="frog-tooltip"
                data-tooltip-content={`By ${creator}`}
            >
                <div className="flex justify-center w-full h-[64px]">
                    <svg data-src={img} {...svgProps} />
                </div>
                <div className="text-lg">{name}</div>
            </div>
            <Tooltip id="frog-tooltip" />
        </>
    );
});

Frog.displayName = "Frog";

export default Frog;
